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

# In-memory session store
sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str

def get_or_create_session(session_id: Optional[str]) -> tuple:
    if session_id is None or session_id not in sessions:
        new_id = session_id or str(uuid.uuid4())
        messages = []
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
        sessions[new_id] = messages
        return new_id, sessions[new_id]
    return session_id, sessions[session_id]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id, messages = get_or_create_session(request.session_id)
    reply, updated_messages = process_message(messages, request.message)
    sessions[session_id] = updated_messages
    return ChatResponse(reply=reply, session_id=session_id)

@app.get("/briefing")
async def briefing():
    data = database.get_briefing_data()
    response = config.client.messages.create(
        model=config.MODEL,
        max_tokens=1024,
        system=config.get_system_prompt(),
        messages=[
            {
                "role": "user",
                "content": f"""Compile a natural conversational morning briefing based on this data:

{json.dumps(data, indent=2, default=str)}

Be concise. Lead with the most important things. Mention streaks if relevant.
If nothing is scheduled say so clearly. Sound like a helpful companion not a robot."""
            }
        ]
    )
    return {"briefing": response.content[0].text}

@app.on_event("shutdown")
async def shutdown():
    for session_id, messages in sessions.items():
        memory.save_memory(messages)
        memory.save_summary(messages)
    print(f"💾 Saved {len(sessions)} sessions on shutdown")

# Static files MUST be last
app.mount("/", StaticFiles(directory="static", html=True), name="static")