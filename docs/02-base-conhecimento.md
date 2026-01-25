# Base de Conhecimento

## Dados Utilizados

Objetivo: Fornecer ao agente contexto estruturado (arquivos locais) e não estruturado (documentos enviados) para permitir o planejamento e a execução de tarefas.

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `tarefas.csv` | CSV | Leitura e Escrita. Contém ID, título, prazo, prioridade e status. É a única fonte que o agente pode modificar via comandos. |
| `rotinas.json` | JSON | Leitura. Estrutura de hábitos ou blocos de tempo ideais. |
| `preferencias_usuario.json` | JSON | Leitura. Define o nome do usuário e configurações gerais de tratamento. |
| `calendario_eventos.csv` | CSV | Leitura. Compromissos com data e descrição. Usado para detectar conflitos de agenda nos próximos 7 dias. |
| `contexto_trabalho.json` | JSON | Leitura. Informações sobre o ambiente de trabalho e sistemas críticos (foco). |
| `Upload de PDF/TXT` | Memória | RAG Temporário. Conteúdo extraído na hora (via pypdf) para dar contexto sobre documentos específicos durante a sessão. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

O agente não consome os arquivos brutos diretamente na LLM. O código realiza um pré-processamento via Pandas para otimizar o uso de tokens e a relevância:
- Filtragem Temporal (Agenda):
    - O código converte a coluna data para datetime.
    -  Aplica um filtro dinâmico: (data >= hoje) & (data <= hoje + 7 dias).
    - Eventos passados ou muito distantes são descartados para não poluir o contexto.
- Saneamento de Tarefas:
    - Filtra apenas tarefas onde status != 'Concluído'.
    - Seleciona apenas colunas úteis (titulo, prazo, prioridade, status) para reduzir o ruído.
    - Tarefas concluídas são contabilizadas apenas no Dashboard (métricas), não no prompt do chat.
- Memória de Documentos:
    - Arquivos PDF são convertidos para texto plano e truncados (limitado aos primeiros 15.000 caracteres no app.py) para caber         na janela de contexto dos modelos locais (Ollama) ou nuvem (Gemini).

---

## Estratégia de Integração
A integração segue o padrão de Injeção de Contexto Dinâmico. A cada interação do chat, o sistema recarrega os dados para garantir que o agente saiba o estado mais atual (ex: se o usuário acabou de concluir uma tarefa).
```python

@st.cache_data(ttl=600) # Cache de 10 min para performance
def obter_contexto_dados():
    # 1. Carregamento Físico
    pref = carregar_json("./data/preferencias_usuario.json")
    tarefas = carregar_csv("./data/tarefas.csv")
    cal = carregar_csv("./data/calendario_eventos.csv")
    
    # 2. Lógica Temporal
    agora = datetime.now()
    limite_dias = agora + timedelta(days=7)
    
    # 3. Transformação para Texto (Stringification)
    # Apenas eventos da próxima semana
    filtro_cal = cal[(cal['data_dt'] >= agora) & (cal['data_dt'] <= limite_dias)]
    cal_txt = filtro_cal.to_string(index=False)
    
    # Apenas tarefas pendentes
    filtro_tarefas = tarefas[tarefas['status'] != 'Concluído']
    tarefas_txt = filtro_tarefas[['titulo', 'prazo', 'prioridade']].to_string(index=False)

    return {
        "pref": pref,
        "cal_txt": cal_txt,
        "tarefas_txt": tarefas_txt
    }

```
### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

### Fluxo de Prompting

- Usuário envia mensagem.
- Sistema:
    - Recupera histórico do chat.
    - Executa obter_contexto_dados() (lê CSV/JSON).
    - Lê st.session_state.doc_text (conteúdo do PDF carregado, se houver).
- Montagem: Combina System Prompt + Dados Estruturados + Mensagem do Usuário.
- Inferência: Envia tudo para Gemini ou Ollama.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```text
[SYSTEM_PROMPT]
Você é o agente Focus... (regras de comportamento, não inventar dados, etc)...

DATA HOJE: 25/01/2026, Sábado
CONTEXTO DO USUÁRIO: Aderaldo | Foco: Sistemas Críticos Service Desk

AGENDA (7 DIAS):
 data        evento             horario
 27/05/2024  Reunião Semanal    10:00
 28/05/2024  Dentista           14:00

TAREFAS PENDENTES:
 titulo                  prazo       prioridade  status
 Relatório Mensal        25/05/2024  Alta        Pendente
 Configurar Backup       26/05/2024  Média       Pendente
 Comprar café            30/05/2024  Baixa       Pendente

CONTEÚDO DOCS:
(Conteúdo extraído do PDF "Manual_Procedimentos.pdf" enviado pelo usuário...)
...O procedimento de backup deve ser realizado via script bash...

HISTÓRICO:
USER: O que eu tenho pra fazer hoje urgente?
ASSISTANT: Você tem o Relatório Mensal para entregar hoje.
USER: Certo, e como eu faço o backup?

USUÁRIO:
(Nova pergunta entra aqui)

```
