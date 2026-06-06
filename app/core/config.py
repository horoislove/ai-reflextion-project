"""Единая точка конфигурации. Значения читаются из .env (см. .env.example)."""
import os

from dotenv import load_dotenv

load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/chat")
HISTORY_WINDOW = int(os.getenv("HISTORY_WINDOW", "20"))