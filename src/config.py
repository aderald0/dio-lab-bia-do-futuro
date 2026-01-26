# src/config.py
from pathlib import Path
import os
import logging

try:
    import streamlit as st  # usado para ler secrets, se estiver rodando no Streamlit
except Exception:
    st = None

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent  # .../src
ROOT_DIR = BASE_DIR.parent                  # raiz do projeto
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"

# Modelos e provedores
DEFAULT_PROVIDER = "Gemini"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_OLLAMA_MODEL = "gpt-oss"
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"

def ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    LOGS_DIR.mkdir(exist_ok=True, parents=True)

def get_gemini_api_key() -> str | None:
    """Tenta obter a chave primeiro do Streamlit secrets, depois do ambiente."""
    api = None
    if st is not None:
        try:
            api = st.secrets.get("GEMINI_API_KEY", None)
        except Exception:
            api = None
    return api or os.getenv("GEMINI_API_KEY")

# Logger único para o app
_logger = None
def get_logger():
    global _logger
    if _logger:
        return _logger

    ensure_dirs()
    logger = logging.getLogger("focus")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    # Arquivo
    fh = logging.FileHandler(LOGS_DIR / "focus.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    _logger = logger
    return _logger
