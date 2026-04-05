import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")  # example, adjust as needed

MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

CIRCUIT_FAILURE_THRESHOLD = int(os.getenv("CIRCUIT_FAILURE_THRESHOLD", "5"))
CIRCUIT_RESET_TIMEOUT_SECONDS = int(os.getenv("CIRCUIT_RESET_TIMEOUT_SECONDS", "60"))

OCR_LANG = os.getenv("OCR_LANG", "eng")