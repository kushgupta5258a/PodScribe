import os
import streamlit as st
from dotenv import load_dotenv

# Load .env only in local development
if os.path.exists(".env"):
    load_dotenv()

ENV = os.getenv("ENV", "DEV")

# ---------------------------
# API KEYS
# ---------------------------

# Priority:
# 1️⃣ Streamlit Cloud secrets
# 2️⃣ Local .env file

try:
    DEEPGRAM_API_KEY = st.secrets["DEEPGRAM_API_KEY"]
except Exception:
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

try:
    OLLAMA_BASE_URL = st.secrets["OLLAMA_BASE_URL"]
except Exception:
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


# ---------------------------
# DATA DIRECTORY
# ---------------------------

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
