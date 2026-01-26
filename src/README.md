# Código da Aplicação


## Estrutura

```
src/
├── app.py              # Aplicação principal (Streamlit/Gradio)
├── agente.py           # Lógica do agente
├── config.py           # Configurações (API keys, etc.)
└── requirements.txt    # Dependências
```

## Exemplo de requirements.txt

```
# src/requirements.txt
streamlit>=1.38.0
pandas>=2.2.0
requests>=2.31.0
google-generativeai>=0.7.2
pypdf>=4.2.0
python-dotenv>=1.0.1
```

## Como Rodar

```bash
# Instalar dependências
pip install pandas requests streamlit google.generativeai pypdf python-dotenv

# Rodar a aplicação
python -m streamlit run .\src\app.py 
```
