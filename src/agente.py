
# src/agente.py
from __future__ import annotations
import json
import time
import requests
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

import streamlit as st

from config import DATA_DIR, get_logger

logger = get_logger()

# ================ Gestão de arquivos ================
def _safe_read_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _safe_read_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def carregar_json(nome_arquivo: str) -> dict:
    return _safe_read_json(DATA_DIR / nome_arquivo)

def carregar_csv(nome_arquivo: str) -> pd.DataFrame:
    return _safe_read_csv(DATA_DIR / nome_arquivo)

def adicionar_nova_tarefa(titulo: str, prazo: str, prioridade: str = "Média"):
    caminho = DATA_DIR / "tarefas.csv"
    try:
        df = carregar_csv("tarefas.csv")
        if df.empty:
            df = pd.DataFrame(columns=["id", "titulo", "prazo", "prioridade", "status"])

        novo_id = (df["id"].max() + 1) if ("id" in df.columns and not df.empty) else 1
        nova_linha = pd.DataFrame([{
            "id": int(novo_id),
            "titulo": titulo,
            "prazo": prazo,
            "prioridade": prioridade,
            "status": "Pendente"
        }])
        df = pd.concat([df, nova_linha], ignore_index=True)
        df.to_csv(caminho, index=False)
        logger.info(f"Tarefa criada: {titulo} (id={novo_id})")
        return True, novo_id
    except Exception as e:
        logger.exception("Falha ao salvar tarefa")
        return False, str(e)

# ================ Leitura de PDF (opcional) ================
try:
    from pypdf import PdfReader
    TEM_PDF = True
except Exception:
    TEM_PDF = False

def ler_pdf(uploaded_file) -> str:
    if not TEM_PDF:
        return "Erro: Biblioteca pypdf não instalada."
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text
    except Exception as e:
        logger.exception("Erro ao ler PDF")
        return f"Erro ao ler PDF: {e}"

# ================ Contexto (cache) ================
@st.cache_data(ttl=600)
def obter_contexto_dados():
    pref = carregar_json("preferencias_usuario.json")
    trab = carregar_json("contexto_trabalho.json")
    rotinas = carregar_json("rotinas.json")
    cal = carregar_csv("calendario_eventos.csv")
    tarefas = carregar_csv("tarefas.csv")

    agora = datetime.now()
    limite_dias = agora + timedelta(days=7)
    hoje_str = agora.strftime("%d/%m/%Y, %A")

    cal_txt = "Nenhum evento próximo."
    if not cal.empty and "data" in cal.columns:
        cal["data_dt"] = pd.to_datetime(cal["data"], dayfirst=True, errors="coerce")
        filtro_cal = cal[(cal["data_dt"] >= agora) & (cal["data_dt"] <= limite_dias)]
        if not filtro_cal.empty:
            cal_txt = filtro_cal.to_string(index=False)

    tarefas_txt = "Nenhuma tarefa pendente."
    if not tarefas.empty and "status" in tarefas.columns:
        filtro_tarefas = tarefas[tarefas["status"] != "Concluído"]
        cols_uteis = [c for c in ["titulo", "prazo", "prioridade", "status"] if c in filtro_tarefas.columns]
        if not filtro_tarefas.empty:
            tarefas_txt = filtro_tarefas[cols_uteis].to_string(index=False)

    return {
        "hoje": hoje_str,
        "pref": pref,
        "trab": trab,
        "rotinas": rotinas,
        "cal_txt": cal_txt,
        "tarefas_txt": tarefas_txt,
    }

# ================ Prompt do agente ================
SYSTEM_PROMPT = """
Você é o agente Focus, um assistente inteligente especializado em organização pessoal e produtividade.

Seu objetivo é ajudar o usuário a:
- Organizar tarefas
- Definir prioridades
- Planejar o dia ou a semana
- Quebrar tarefas grandes em passos menores
- Revisar progresso e criar rotinas realistas

Você NÃO executa tarefas, NÃO cria compromissos automaticamente e NÃO acessa sistemas externos.
Você atua exclusivamente como apoio ao planejamento e organização.

====================
FONTE DE INFORMAÇÕES
====================
- Você só pode utilizar os dados fornecidos no contexto da conversa.
- Esses dados podem incluir: tarefas, agenda, preferências do usuário, rotinas, bloqueios e progresso.
- Nunca invente tarefas, compromissos ou preferências que não estejam nos dados.
- Se alguma informação necessária não estiver disponível, pergunte de forma objetiva.

========
REGRAS
========
1. Baseie todas as respostas exclusivamente nos dados fornecidos no contexto.
2. Nunca assuma horários, prazos ou prioridades sem confirmação explícita.
3. Não crie compromissos nem altere agendas sem autorização clara do usuário.
4. Sugira no máximo o número de tarefas definido nas preferências do usuário.
5. Sempre proponha opções, nunca ordens.
6. Utilize blocos de foco curtos (ex: 25 minutos) e pausas.
7. Se houver conflitos de horário, avise o usuário antes de sugerir qualquer plano.
8. Caso a solicitação esteja fora do escopo, explique educadamente sua limitação.

====================
ESTILO DE COMUNICAÇÃO
====================
- Tom direto, positivo e acolhedor
- Linguagem simples e prática
- Passos claros e acionáveis
- Sem julgamentos ou cobranças
"""

# ================ Integração com LLMs ================
def perguntar_llm(
    msg: str,
    historico: list[dict],
    dados_ctx: dict,
    doc_contexto: str,
    provider: str,
    model_name: str,
    gemini_obj=None,
    ollama_url: str | None = None,
) -> str:
    historico_txt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in historico])

    prompt = f"""
{SYSTEM_PROMPT}

DATA HOJE: {dados_ctx['hoje']}
CONTEXTO DO USUÁRIO: {dados_ctx['pref'].get('nome', 'Usuário')} | Foco: {dados_ctx['trab'].get('sistemas_criticos', '')}
AGENDA (7 DIAS): {dados_ctx['cal_txt']}
TAREFAS PENDENTES: {dados_ctx['tarefas_txt']}
CONTEÚDO DOCS: {doc_contexto}
HISTÓRICO: {historico_txt}

USUÁRIO: {msg}
"""

    try:
        t0 = time.time()
        if provider == "Gemini":
            if not gemini_obj:
                return "Erro: Modelo Gemini não inicializado."
            response = gemini_obj.generate_content(prompt)
            texto = getattr(response, "text", "") or "Sem resposta do Gemini."
        elif provider == "Ollama":
            payload = {"model": model_name, "prompt": prompt, "stream": False}
            resp = requests.post(ollama_url, json=payload, timeout=120)
            if resp.status_code == 200:
                texto = resp.json().get("response", "Sem resposta do Ollama.")
            else:
                texto = f"Erro Ollama: {resp.status_code} - {resp.text}"
        else:
            texto = "Provedor não suportado."

        dt = (time.time() - t0) * 1000
        logger.info(f"LLM provider={provider} model={model_name} prompt_chars={len(prompt)} resp_chars={len(texto)} latency_ms={dt:.0f}")
        return texto

    except Exception as e:
        logger.exception("Erro fatal na LLM")
        return f"Erro fatal na LLM: {e}"
