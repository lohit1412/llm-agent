import json
import os
import numpy as np
import config
from sklearn.metrics.pairwise import cosine_similarity

MEMORY_FILE = "memory.json"
EMBEDDINGS_FILE = "embeddings.npy"
SUMMARY_FILE = "memory_summary.txt"

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

def save_memory(messages):
    meaningful = [m for m in messages if is_worth_saving(m)]

    if not meaningful:
        return
    
    clean_messages = []
    embeddings = []

    for msg in meaningful:
        clean_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
        if "embedding" in msg:
            embeddings.append(msg["embedding"])
        else:
            embeddings.append(config.embedding_model.encode(msg["content"]).tolist())
    
    with open(MEMORY_FILE, "w") as f:
        json.dump(clean_messages, f, indent=2)

    np.save(EMBEDDINGS_FILE, np.array(embeddings))
    
    print(f"💾 Saved {len(clean_messages)} meaningful messages to memory")

def load_relevant_memory(query, top_k = 5):
    if not os.path.exists(MEMORY_FILE):
        return []
    if not os.path.exists(EMBEDDINGS_FILE):
        return []
    
    with open(MEMORY_FILE, "r") as f:
        messages = json.load(f)
    
    embeddings = np.load(EMBEDDINGS_FILE)

    if len(messages) == 0:
        return []
    
    # Encode query and find most similar messages
    query_embedding = config.embedding_model.encode(query).reshape(1, -1)
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    # Get top_k most relevant indices
    top_indices = similarities.argsort()[-top_k:][::-1]

    # Return relevant messages sorted by original order
    relevant = [messages[i] for i in sorted(top_indices)]

    return relevant

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def summarize_memory(messages):
    if not messages:
        return None
    
    conversation_text = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in messages
    ])
    
    response = config.client.messages.create(
        model=config.MODEL,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""Summarize this conversation history concisely.
                Focus on: who the user is, key facts about them, and main topics discussed.
                Keep it under 150 words.
                CONVERSATION: {conversation_text}"""
            }
        ]
    )
    
    return response.content[0].text

def load_summary():
    """Load summary from disk on startup"""
    if not os.path.exists(SUMMARY_FILE):
        return None
    with open(SUMMARY_FILE, "r") as f:
        return f.read()

def save_summary(messages):
    if not messages:
        return
    
    # Load existing summary if it exists
    existing_summary = load_summary()
    
    # Build the new conversation text
    conversation_text = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in messages
        if isinstance(msg.get("content"), str)
    ])
    
    # Combine existing summary with new conversation
    if existing_summary:
        prompt = f"""You are maintaining a running memory summary of conversations with a user.
        EXISTING SUMMARY: {existing_summary}
        NEW CONVERSATION: {conversation_text}
        Update the summary by merging the existing summary with the new conversation.
        - Keep key facts about the user (name, preferences, goals)
        - Add important new topics discussed
        - Remove outdated or redundant information
        - Keep it under 500 words
        - Write it as a concise factual summary, not a narrative"""
    else:
        prompt = f"""Summarize this conversation concisely.
        Focus on: who the user is, key facts about them, and main topics discussed.
        Keep it under 500 words.

        CONVERSATION:
        {conversation_text}"""
    
    response = config.client.messages.create(
        model=config.MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    
    summary = response.content[0].text
    
    with open(SUMMARY_FILE, "w") as f:
        f.write(summary)
    
    print(f"📝 Updated memory summary")