from enum import Enum
from dataclasses import dataclass
from typing import Any
from datetime import datetime

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

def user_message(content):
    return {"role": Role.USER.value, "content": content}

def assistant_message(content):
    return {"role": Role.ASSISTANT.value, "content": content}

def tool_result_message(tool_results):
    return {
        "role": Role.USER.value, 
        "content": tool_results
    }

#---------- Result Types ----------

@dataclass
class Success:
    data: Any
    tool_name: str
    timestamp: str = None

    def __post_init__(self):
        self.timestamp = datetime.now().isoformat()

@dataclass
class Error:
    message: str
    tool_name: str
    timestamp: str = None

    def __post_init__(self):
        self.timestamp = datetime.now().isoformat()

def is_success(result) -> bool:
    return isinstance(result, Success)

def log_tool_call(result):
    status = "✅" if is_success(result) else "❌"
    print(f"{status} [{result.timestamp}] {result.tool_name}"
          f"{'success' if is_success(result) else result.message}")
