import memory
import uuid
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from agent import process_message

app = FastAPI()

# In-memory session store
sessions = {}

# Request Model - what the client sends
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

# Response model - what we send back
class ChatResponse(BaseModel):
    reply: str
    session_id: str

# Load Summary on startup

def get_or_create_session(session_id: Optional[str]) -> tuple:
    # Create new session if none provided
    if session_id is None or session_id not in sessions:
        new_id = session_id or str(uuid.uuid4())
        messages = []
        # Load summary context for new sessions
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

# Chat endpoiunt
@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):
    session_id, messages = get_or_create_session(request.session_id)
    reply, updated_messages = process_message(
        messages,
        request.message
    )
    sessions[session_id] = updated_messages
    return ChatResponse(reply=reply, session_id=session_id)

# Save memory on shutdown
@app.on_event("shutdown")
async def shutdown():
    # Save all active sessions on shutdown
    for session_id, messages in sessions.items():
        memory.save_memory(messages)
        memory.save_summary(messages)
    print(f"💾 Saved {len(sessions)} sessions on shutdown")

# Static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")