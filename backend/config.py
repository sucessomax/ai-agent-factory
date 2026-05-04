import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

VERCEL = os.getenv("VERCEL", "0")
VERCEL_URL = os.getenv("VERCEL_URL", "")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment")