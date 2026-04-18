import memory
import uuid
import json
import config
import database
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agent import process_message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory cache (hybrid) ─────────────────────────
sessions_cache = {}
SYNC_EVERY = 10  # sync to DB every N messages

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str

# ── Session Management ───────────────────────────────

def get_or_create_session(session_id: Optional[str]) -> tuple:
    # Check RAM cache first
    if session_id and session_id in sessions_cache:
        return session_id, sessions_cache[session_id]

    # Try loading from Supabase
    if session_id:
        messages = database.load_session_from_db(session_id)
        if messages:
            sessions_cache[session_id] = messages
            return session_id, messages

    # Create new session
    new_id = session_id or str(uuid.uuid4())
    messages = []

    # Load memory summary for context
    summary = memory.load_summary()
    if summary:
        messages.append({
            "role": "user",
            "content": f"Here is context from our previous conversations: {summary}"
        })
        messages.append({
            "role": "assistant",
            "content": "Understood. I have context from our previous conversations and will use it naturally."
        })

    sessions_cache[new_id] = messages
    # Save new session to DB immediately
    database.save_session_to_db(new_id, messages)
    return new_id, messages

def should_sync(messages):
    # Sync every SYNC_EVERY messages
    return len(messages) % SYNC_EVERY == 0

# ── Endpoints ────────────────────────────────────────

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id, messages = get_or_create_session(request.session_id)

    reply, updated_messages = process_message(messages, request.message)
    sessions_cache[session_id] = updated_messages

    # Sync to DB periodically
    if should_sync(updated_messages):
        database.save_session_to_db(session_id, updated_messages)

    return ChatResponse(reply=reply, session_id=session_id)

@app.get("/briefing")
async def briefing():
    data = database.get_briefing_data()
    summary = memory.load_summary() or ""

    response = config.client.messages.create(
        model=config.MODEL,
        max_tokens=1024,
        system=config.get_system_prompt(),
        messages=[
            {
                "role": "user",
                "content": f"""{config.BRIEFING_PROMPT}

                USER CONTEXT: {summary}

                DATA: {json.dumps(data, indent=2, default=str)}"""
            }
        ]
    )
    return {"briefing": response.content[0].text}

@app.on_event("shutdown")
async def shutdown():
    # Save all active sessions to Supabase on shutdown
    for session_id, messages in sessions_cache.items():
        database.save_session_to_db(session_id, messages)
        memory.save_memory(messages)
        memory.save_summary(messages)
    print(f"💾 Saved {len(sessions_cache)} sessions to Supabase on shutdown")

# Static files MUST be last
app.mount("/", StaticFiles(directory="static", html=True), name="static")