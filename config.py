import os
from anthropic import Anthropic
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY").strip())

with open("system_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
MAX_ITERATIONS = 10
