# 🪶 Quill — AI Agent

> **Ask it about my work. It actually knows.**

Quill is an AI agent that knows about me inside out — ask it about my projects, skills, or experience and it answers from verified context instead of guessing, and falls back to general conversation when you're just saying hi.

**Live demo:** [quill-aiagent.vercel.app](https://quill-aiagent.vercel.app)

---

## ✨ Features (v1.0)

- **Smart routing** — a lightweight classifier decides whether you're asking about the portfolio or just chatting, on every single message
- **Grounded answers** — portfolio questions are answered from a vector store built on real project docs, not from the model's imagination
- **No hallucinated history** — if there isn't enough verified context to answer confidently, Quill says so instead of making something up
- **Natural fallback** — general chit-chat (greetings, small talk, unrelated questions) gets a normal conversational response
- **Fast, lightweight inference** — chat completions run through DeepSeek via OpenRouter

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI |
| Vector store | ChromaDB |
| Embeddings | Hugging Face Inference API |
| Chat completions | OpenRouter (DeepSeek) |
| Frontend | React + Vite |
| Backend hosting | Render |
| Frontend hosting | Vercel |

---

## 🗂️ Project Structure

```
Quill/
├── backend/
│   ├── app.py                  # FastAPI app, /chat endpoint
│   ├── router.py                # Classifies queries as "portfolio" or "general"
│   ├── llm.py                   # OpenRouter client setup
│   ├── prompts.py                # System prompt
│   ├── rag/
│   │   ├── ingest.py             # Loads portfolio docs into the vector store
│   │   ├── retriever.py          # Retrieves relevant context for a query
│   │   ├── vectorstore.py        # Chroma + embedding setup
│   │   ├── portfolio_docs/       # Source documents for retrieval
│   │   └── chroma_db/            # Persisted vector store
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── QuillChat.jsx     # Main chat interface
│       │   └── MessageBubble.jsx # Individual message rendering
│       ├── App.jsx
│       └── main.jsx
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js
- Python 3.x
- An [OpenRouter](https://openrouter.ai) API key
- A [Hugging Face](https://huggingface.co) API token

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:

```env
OPENROUTER_API_KEY=your_openrouter_key
HF_API_TOKEN=your_huggingface_token
```

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The backend runs on `http://localhost:8000`.

### Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env` file in the `frontend/` folder:

```env
VITE_API_URL=http://localhost:8000
```

Start the dev server:

```bash
npm run dev
```

---

## 🔄 How It Works

1. A message comes in through the `/chat` endpoint
2. The router classifies it as **portfolio** or **general**
3. If **portfolio** — the retriever pulls relevant chunks from the Chroma vector store (built from the project docs in `portfolio_docs/`)
4. If there's enough verified context, the LLM answers grounded in that context; if not, Quill says it doesn't have enough information rather than guessing
5. If **general** — the message skips retrieval entirely and goes straight to the LLM for a normal conversational reply
6. Either way, the response is generated through DeepSeek via OpenRouter and streamed back to the React frontend

---

## 🌐 Deployment

Quill is live! You can try it here: **[quill-aiagent.vercel.app](https://quill-aiagent.vercel.app)**
<img width="1918" height="906" alt="image" src="https://github.com/user-attachments/assets/7b6aac06-b6f2-43c8-a4fa-4a91b2a01a3f" />


---

## 🗺️ Roadmap

### v2.0 (Coming Soon)

- Conversation memory across turns for more natural follow-ups
- Easier portfolio doc management (add/update without re-running ingest manually)
- Lightweight analytics on what people actually ask
- Multi-language support
- Inline source citations so answers point back to the exact doc they came from

---

## 📄 License & Copyright

© 2026 Divyasree Manikandan. All rights reserved.

This project and its source code are the intellectual property of the author. Unauthorized copying, distribution, or use of this codebase, in whole or in part, without explicit written permission is prohibited.

---

*Made with ❤️, caffeine, and several strongly worded conversations with deployment.*
