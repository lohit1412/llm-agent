import json
import os

MEMORY_FILE = "memory.json"

def save_memory(messages):
    serializable = []
    for message in messages:
        if isinstance(message["content"], str):
            serializable.append(message)
    with open(MEMORY_FILE, "w") as f:
        json.dump(serializable, f, indent=2)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)
