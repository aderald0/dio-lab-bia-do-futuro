# 🐉 Focus - Agente de Produtividade Pessoal com IA

> Projeto desenvolvido como parte do desafio de Agentes Inteligentes com IA Generativa.

O **Focus** é um assistente virtual proativo que utiliza Inteligência Artificial para ajudar na organização pessoal, priorização de tarefas e gestão de tempo, integrando dados locais (agenda, tarefas) com análise de documentos (RAG).

---

## 📋 O Problema
Profissionais e estudantes frequentemente sofrem com a sobrecarga de informações, dificuldade em priorizar tarefas e desconexão entre o planejamento (agenda) e a execução (lista de tarefas).

## 💡 A Solução
O Focus atua como um "par organizador" que:
- **Centraliza** tarefas, rotinas e calendário.
- **Analisa** documentos (PDFs) para extrair prazos e contextos.
- **Executa** ações reais (criação de tarefas) via comandos em linguagem natural.
- **Protege** a privacidade com opção de execução local (Ollama).

---
## 🏗️ Arquitetura e Tecnologias

O projeto utiliza uma arquitetura híbrida de injeção de contexto (RAG) e chamadas de função (Function Calling).

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **Interface** | Streamlit | Chat interativo, Dashboard de métricas e Upload de arquivos. |
| **Cérebro (LLM)** | Google Gemini / Ollama | Interpretação de intenções e geração de respostas. |
| **Dados** | Pandas (CSV/JSON) | Manipulação de tarefas e agenda em tempo real. |
| **RAG** | PyPDF | Extração de texto de documentos para contexto. |

### Diagrama de Fluxo
```mermaid
flowchart TD
    User[Usuário] -->|Chat/Arquivo| UI[Interface Streamlit]
    UI --> Context[Montador de Contexto]
    Data[(CSVs e JSONs)] <--> Context
    Docs[PDF Upload] --> Context
    Context --> LLM["IA (Gemini/Ollama)"]
    LLM -->|Resposta Texto| UI
    LLM -->|Comando JSON| Action[Executor de Ações]
    Action -->|Criar Tarefa| Data
```
---
## O Que Você Deve Entregar

### 1. Documentação do Agente

Defina **o que** seu agente faz e **como** ele funciona:

- **Caso de Uso:** Qual problema ele resolve? (ex: consultoria de investimentos, planejamento de metas, alertas de gastos)
- **Persona e Tom de Voz:** Como o agente se comporta e se comunica?
- **Arquitetura:** Fluxo de dados e integração com a base de conhecimento
- **Segurança:** Como evitar alucinações e garantir respostas confiáveis?

📄 **Template:** [`docs/01-documentacao-agente.md`](./docs/01-documentacao-agente.md)

---

### 2. Base de Conhecimento

Utilize os **dados mockados** disponíveis na pasta [`data/`](./data/) para alimentar seu agente:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `tarefas.csv` | CSV | Leitura e Escrita. Contém ID, título, prazo, prioridade e status. É a única fonte que o agente pode modificar via comandos. |
| `rotinas.json` | JSON | Leitura. Estrutura de hábitos ou blocos de tempo ideais. |
| `preferencias_usuario.json` | JSON | Leitura. Define o nome do usuário e configurações gerais de tratamento. |
| `calendario_eventos.csv` | CSV | Leitura. Compromissos com data e descrição. Usado para detectar conflitos de agenda nos próximos 7 dias. |
| `contexto_trabalho.json` | JSON | Leitura. Informações sobre o ambiente de trabalho e sistemas críticos (foco). |
| `Upload de PDF/TXT` | Memória | RAG Temporário. Conteúdo extraído na hora (via pypdf) para dar contexto sobre documentos específicos durante a sessão. |


📄 **Template:** [`docs/02-base-conhecimento.md`](./docs/02-base-conhecimento.md)

---

### 3. Prompts do Agente

Documente os prompts que definem o comportamento do seu agente:

- **System Prompt:** Instruções gerais de comportamento e restrições
- **Exemplos de Interação:** Cenários de uso com entrada e saída esperada
- **Tratamento de Edge Cases:** Como o agente lida com situações limite

📄 **Template:** [`docs/03-prompts.md`](./docs/03-prompts.md)

---

### 4. Aplicação Funcional

Desenvolva um **protótipo funcional** do seu agente:

- Chatbot interativo (sugestão: Streamlit, Gradio ou similar)
- Integração com LLM (via API ou modelo local)
- Conexão com a base de conhecimento

📁 **Pasta:** [`src/`](./src/)

---

### 5. Avaliação e Métricas

Descreva como você avalia a qualidade do seu agente:

**Métricas Sugeridas:**
- Precisão/assertividade das respostas
- Taxa de respostas seguras (sem alucinações)
- Coerência com o perfil do cliente

📄 **Template:** [`docs/04-metricas.md`](./docs/04-metricas.md)
📁 **Uso da API:** [`docs/`](./docs/Uso_da_API.pdf)
📁 **Teste do Agente:** [`docs/`](./docs/Testes_do_agente_Focus.pdf)

---

### 6. Pitch

Grave um **pitch de 3 minutos** (estilo elevador) apresentando:

- Qual problema seu agente resolve?
- Como ele funciona na prática?
- Por que essa solução é inovadora?

📄 **Template:** [`docs/05-pitch.md`](./docs/05-pitch.md)

---

## Ferramentas Sugeridas

Todas as ferramentas abaixo possuem versões gratuitas:

| Categoria | Ferramentas |
|-----------|-------------|
| **LLMs** | [ChatGPT](https://chat.openai.com/), [Copilot](https://copilot.microsoft.com/), [Gemini](https://gemini.google.com/), [Claude](https://claude.ai/), [Ollama](https://ollama.ai/) |
| **Desenvolvimento** | [Streamlit](https://streamlit.io/), [Gradio](https://www.gradio.app/), [Google Colab](https://colab.research.google.com/) |
| **Orquestração** | [LangChain](https://www.langchain.com/), [LangFlow](https://www.langflow.org/), [CrewAI](https://www.crewai.com/) |
| **Diagramas** | [Mermaid](https://mermaid.js.org/), [Draw.io](https://app.diagrams.net/), [Excalidraw](https://excalidraw.com/) |

---

## Estrutura do Repositório

```
📁 focus-agente-produtividade/
│
├── 📄 README.md              # Documentação principal
├── 📄 requirements.txt       # Dependências do Python
│
├── 📁 data/                          # Dados mockados para o agente
│   ├── tarefas.csv                   # Banco de tarefas (Leitura/Escrita)
│   ├── calendario_eventos.csv        # Agenda de compromissos (Leitura)
│   ├── rotinas.json                  # Blocos de rotina diária
│   ├── contexto_trabalho.json        # Dados do ambiente profissional
│   └── preferencias_usuario.json     # Configurações de perfil
├── 📁 logs/                          # Dados de LOGs
│   ├── focus.log                     # Log de eventos
|
├── 📁 docs/                          # Documentação do projeto
│   ├── 01-documentacao-agente.md     # Caso de uso e arquitetura
│   ├── 02-base-conhecimento.md       # Estratégia de dados
│   ├── 03-prompts.md                 # Engenharia de prompts
│   ├── 04-metricas.md                # Avaliação e métricas
│   └── 05-pitch.md                   # Roteiro do pitch
│
├── 📁 src/                           # Código da aplicação
│   ├── app.py                        # Interface (Streamlit) e orquestração
│   ├── agente.py                     # Lógica do agente (dados, prompt, LLM, comandos)
|   ├── config.py                     # Configuração (paths, API key, logger)
|   └── requirements.txt              # Dependências
│
├── 📁 assets/                        # Imagens e diagramas
│   └── ...
│
└── 📁 examples/                      # Referências e exemplos
    └── README.md
```

---

## Dicas Finais

1. **Comece pelo prompt:** Um bom system prompt é a base de um agente eficaz
2. **Use os dados mockados:** Eles garantem consistência e evitam problemas com dados sensíveis
3. **Foque na segurança:** No setor financeiro, evitar alucinações é crítico
4. **Teste cenários reais:** Simule perguntas que um cliente faria de verdade
5. **Seja direto no pitch:** 3 minutos passam rápido, vá ao ponto
