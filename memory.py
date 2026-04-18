import json
import config
import database
from datetime import date

TRIVIAL_MESSAGES = {
    "ok", "hi", "hey", "thanks", "bye", "exit",
    "quit", "yes", "no", "sure", "great", "cool",
    "okay", "alright", "got it", "noted"
}

def is_worth_saving(message):
    if not isinstance(message.get("content"), str):
        return False
    content = message["content"].strip().lower()
    if content in TRIVIAL_MESSAGES:
        return False
    if len(content) < 10:
        return False
    return True

# ── Save Memory ──────────────────────────────────────

def save_memory(messages, user_id="default_user"):
    meaningful = [m for m in messages if is_worth_saving(m)]
    if not meaningful:
        return

    for msg in meaningful:
        content = msg["content"]
        role = msg["role"]
        # Compute embedding
        embedding = config.embedding_model.encode(content).tolist()
        database.save_embedding(content, role, embedding, user_id)

    print(f"💾 Saved {len(meaningful)} messages to Supabase embeddings")

# ── Load Relevant Memory (RAG) ───────────────────────

def load_relevant_memory(query, top_k=5, user_id="default_user"):
    query_embedding = config.embedding_model.encode(query).tolist()
    results = database.search_embeddings(query_embedding, top_k, user_id)

    if not results:
        return []

    # Convert to message format
    messages = []
    for r in results:
        messages.append({
            "role": r["role"],
            "content": r["content"]
        })
    return messages

# ── Summary ──────────────────────────────────────────

def load_summary(user_id="default_user"):
    return database.load_summary_from_db(user_id)

def save_summary(messages, user_id="default_user"):
    if not messages:
        return

    existing_summary = load_summary(user_id)

    conversation_text = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in messages
        if isinstance(msg.get("content"), str)
    ])

    memory_prompt = load_memory_prompt()

    if existing_summary:
        prompt = f"""{memory_prompt}

EXISTING SUMMARY:
{existing_summary}

NEW CONVERSATION:
{conversation_text}

Update the summary."""
    else:
        prompt = f"""{memory_prompt}

CONVERSATION:
{conversation_text}

Create the initial summary."""

    response = config.client.messages.create(
        model=config.MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.content[0].text
    database.save_summary_to_db(summary, user_id)
    print(f"📝 Updated memory summary in Supabase")

def load_memory_prompt():
    try:
        with open("memory_prompt.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Summarize this conversation. Focus on who the user is, key facts, and main topics. Keep under 500 words."

# ── Recent Memory ────────────────────────────────────

def load_recent_memory(n=10, user_id="default_user"):
    """Load last N messages from Supabase embeddings table"""
    result = database.supabase.table("embeddings").select("content, role").eq("user_id", user_id).order("created_at", desc=True).limit(n).execute()
    if not result.data:
        return []
    # Reverse to get chronological order
    messages = [{"role": r["role"], "content": r["content"]} for r in reversed(result.data)]
    return messages