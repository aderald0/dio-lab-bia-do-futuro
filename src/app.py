
# src/app.py
import json
import uuid
import io

import streamlit as st
import pandas as pd
import google.generativeai as genai

from config import (
    DEFAULT_PROVIDER, DEFAULT_GEMINI_MODEL, DEFAULT_OLLAMA_MODEL,
    DEFAULT_OLLAMA_URL, get_gemini_api_key
)
from agente import (
    perguntar_llm, obter_contexto_dados, adicionar_nova_tarefa, ler_pdf,
    carregar_csv
)

# ================= CONFIG DA PÁGINA =================
st.set_page_config(
    page_title="Focus - Agente Inteligente",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🐉 Focus")

# ================= SIDEBAR (LLM) =================
with st.sidebar:
    st.header("⚙️ Cérebro da IA")

    llm_provider = st.selectbox("Escolha o Provedor", ["Gemini", "Ollama"], index=0 if DEFAULT_PROVIDER == "Gemini" else 1)

    active_gemini_model = None
    current_model_name = ""
    ollama_url = DEFAULT_OLLAMA_URL

    if llm_provider == "Gemini":
        current_model_name = st.text_input("Modelo Gemini", value=DEFAULT_GEMINI_MODEL)
        api_key = get_gemini_api_key()
        if not api_key:
            api_key = st.text_input("Cole sua Gemini API Key", type="password")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                active_gemini_model = genai.GenerativeModel(current_model_name)
                st.success("Gemini conectado!")
            except Exception as e:
                st.error(f"Erro config Gemini: {e}")
        else:
            st.warning("API Key necessária.")
    else:
        current_model_name = st.text_input("Modelo Ollama", value=DEFAULT_OLLAMA_MODEL)
        ollama_url = st.text_input("URL Ollama", value=DEFAULT_OLLAMA_URL)
        st.info("Certifique-se de que o Ollama está rodando localmente.")

    st.markdown("---")
    if st.button("Limpar Histórico"):
        st.session_state.conversas = {str(uuid.uuid4()): []}
        st.session_state.conversa_atual = list(st.session_state.conversas.keys())[0]
        st.rerun()

# ================= ESTADO DE SESSÃO =================
if "conversas" not in st.session_state:
    st.session_state.conversas = {str(uuid.uuid4()): []}
    st.session_state.conversa_atual = list(st.session_state.conversas.keys())[0]
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

# ================= ABAS =================
tab_chat, tab_dash, tab_docs = st.tabs(["💬 Chat & Comandos", "📊 Dashboard", "📂 Documentos"])

# ---- ABA: DOCUMENTOS ----
with tab_docs:
    st.header("🧠 Adicionar Conhecimento")
    uploaded_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt"])
    if uploaded_file and st.button("Processar Arquivo"):
        with st.spinner("Lendo..."):
            if uploaded_file.type == "application/pdf":
                txt = ler_pdf(uploaded_file)
            else:
                txt = uploaded_file.read().decode("utf-8", errors="ignore")
            st.session_state.doc_text = txt[:15000]
            st.success("Documento memorizado!")

# ---- ABA: DASHBOARD ----
with tab_dash:
    st.header("📊 Métricas")
    df_t = carregar_csv("tarefas.csv")
    if not df_t.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Pendentes", int((df_t["status"] != "Concluído").sum()))
        c2.metric("Concluídas", int((df_t["status"] == "Concluído").sum()))
        if "prioridade" in df_t.columns:
            c3.metric("Alta Prioridade", int(((df_t["status"] != "Concluído") & (df_t["prioridade"] == "Alta")).sum()))
            st.bar_chart(df_t["prioridade"].value_counts())
        else:
            c3.metric("Alta Prioridade", 0)
            st.info("Coluna 'prioridade' não encontrada em tarefas.csv")
    else:
        st.info("Sem dados de tarefas.")

# ---- ABA: CHAT ----
with tab_chat:
    mensagens = st.session_state.conversas[st.session_state.conversa_atual]

    for msg in mensagens:
        avatar = "🐉" if msg["role"] == "assistant" else "👤"
        st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

    if pergunta := st.chat_input("Digite sua mensagem..."):
        mensagens.append({"role": "user", "content": pergunta})
        st.chat_message("user", avatar="👤").write(pergunta)

        with st.chat_message("assistant", avatar="🐉"):
            with st.status("Processando...", expanded=True) as status:
                ctx = obter_contexto_dados()

                resp_raw = perguntar_llm(
                    msg=pergunta,
                    historico=mensagens,
                    dados_ctx=ctx,
                    doc_contexto=st.session_state.doc_text,
                    provider=llm_provider,
                    model_name=current_model_name,
                    gemini_obj=active_gemini_model,
                    ollama_url=ollama_url,
                )

                texto_final = resp_raw
                # Tenta interpretar JSON de comando
                try:
                    clean = resp_raw.replace("```json", "").replace("```", "").strip()
                    if "{" in clean and "}" in clean:
                        i0 = clean.find("{")
                        i1 = clean.rfind("}") + 1
                        cmd = json.loads(clean[i0:i1])
                        if cmd.get("acao") == "criar_tarefa":
                            d = cmd["dados"]
                            ok, i = adicionar_nova_tarefa(d["titulo"], d["prazo"], d.get("prioridade", "Média"))
                            if ok:
                                texto_final = f"✅ Tarefa Criada: **{d['titulo']}** ({d['prazo']})"
                                st.cache_data.clear()
                            else:
                                texto_final = f"❌ Erro ao salvar: {i}"
                except Exception:
                    pass

                status.update(label="Concluído", state="complete", expanded=False)

            st.write(texto_final)
            mensagens.append({"role": "assistant", "content": texto_final})
