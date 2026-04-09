# Athena — Agentic AI Assistant

Athena is a personal AI assistant built from scratch in Python. She can search the web for real-time information, convert timezones, perform calculations, and remember you across conversations. Built on top of Anthropic's Claude API, Athena uses an agentic loop — she reasons about what tools to use, chains them together, and returns accurate answers without hallucinating.

This project was built as a hands-on learning exercise in agentic AI engineering

> **Note:** This is a trail project — built for hands-on exploration of agentic AI engineering concepts. The goal is learning by doing, not production readiness. Expect rough edges and ongoing changes as new concepts get added.


## What Athena Can Do

- **Web search** — real-time information via Tavily
- **Timezone conversion** — accurate conversion in Python, not Claude
- **Calculations** — math evaluated in Python, not Claude
- **Multi-tool chaining** — chains multiple tools in one request automatically
- **Persistent memory** — remembers you across sessions via summarized context and semantic search
- **REST API** — accessible via FastAPI with session management
- **Web UI** — chat interface served at `http://localhost:8000`

## Architecture

```
athena/
├── main.py              # CLI entry point
├── api.py               # FastAPI HTTP server + session management
├── agent.py             # Agent loop, tool orchestration
├── tools.py             # Tool functions (search, timezone, calculator)
├── tool_definitions.py  # Tool schemas for Claude
├── memory.py            # Memory system (save, load, summarize, semantic search)
├── models.py            # Data structures (Role, Success, Error, message helpers)
├── config.py            # Shared config, API clients, embedding model
├── system_prompt.txt    # Athena's personality and constraints
├── memory_prompt.txt    # Instructions for memory summarization
└── static/              # Web UI (HTML, CSS, JS)
    ├── index.html
    ├── style.css
    └── app.js
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/lohit1412/llm-agent.git
cd llm-agent
```

**2. Create virtual environment**
```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add API keys**

Create a `.env` file in the root:
```
ANTHROPIC_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```
- Anthropic API key: [console.anthropic.com](https://console.anthropic.com)
- Tavily API key: [tavily.com](https://tavily.com)

## How to Run

**Web UI (recommended)**
```bash
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000` in your browser.

**CLI**
```bash
python main.py
```

## API

**POST /chat**
```json
{
  "message": "What is Man United's next fixture?",
  "session_id": "optional-existing-session-id"
}
```

Response:
```json
{
  "reply": "Man United play...",
  "session_id": "abc-123"
}
```

Pass the returned `session_id` in subsequent requests to maintain conversation context.

Interactive API docs available at `http://127.0.0.1:8000/docs`.

## Memory System

Athena uses a three-layer memory architecture:

- **Summary** — compressed context injected at session start
- **Semantic search** — embedding-based retrieval of relevant past messages
- **Raw storage** — all meaningful messages saved to `memory.json` + `embeddings.npy`

Memory files (`memory.json`, `embeddings.npy`, `memory_summary.txt`) are personal and excluded from the repo via `.gitignore`.

## Contributing

**Branch naming convention:**
user/type/description

1. Fork or branch from `main`
2. Make your changes
3. Submit a pull request to `main`
4. PRs require review before merging

## Known Limitations

- Sessions are stored in memory — lost on server restart (SQLite persistence planned)
- Memory summary is global — not per user (multi-user support planned)
- No authentication on the API endpoint

## What's Next

- [ ] SQLite session persistence
- [ ] Per-user memory isolation
- [ ] Document ingestion — feed Athena your own files
- [ ] MemPalace integration for structured memory
- [ ] Multimodal tools — vision, image understanding
- [ ] Deployment guide