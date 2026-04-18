import os
from anthropic import Anthropic
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from datetime import datetime

load_dotenv()

os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY").strip())

SUPABASE_URL =  os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

with open("system_prompt.txt", "r") as f:
    _base_prompt = f.read()

with open("briefing_prompt.txt", "r") as f:
    BRIEFING_PROMPT = f.read()

def get_system_prompt():
    today = datetime.now().strftime("%A, %B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p")
    return f"Today us {today}. Current time is {current_time} CST. \n\n{_base_prompt}"

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
MAX_ITERATIONS = 10
