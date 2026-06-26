from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os, re, time, random
from dotenv import load_dotenv
from difflib import get_close_matches
from contextlib import asynccontextmanager

from router import classify_query, GREETINGS
from prompts import QUILL_SYSTEM_PROMPT
from rag.retriever import retrieve_portfolio_context
from fastapi.middleware.cors import CORSMiddleware
from llm import client

load_dotenv()

# Warm up on startup, not on first request
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Warming up vectorstore + embedding model...")
    from rag.vectorstore import get_vectorstore
    get_vectorstore()
    print("Quill is ready.")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://quill-aiagent.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

GREETING_RESPONSES = [
    "Hey! I'm Quill! Ask me anything about Divya's work, projects, or skills!",
    "Hi there! I'm Quill, Divya's AI assistant. What would you like to know?",
    "Hello! Ask me about Divya's projects, experience, or skills and I'll do my best to help!",
]

def has_context(context: str) -> bool:
    return bool(context and len(context.strip()) > 30)

def is_greeting(msg: str) -> bool:
    normalized = re.sub(r'(.)\1+', r'\1', msg.lower().strip())
    return (
        normalized in GREETINGS
        or msg.lower().strip() in GREETINGS
        or bool(get_close_matches(normalized, GREETINGS, n=1, cutoff=0.7))
    )

def build_user_content(mode: str, context: str, message: str) -> str:
    return f"Mode: {mode}\n\nPortfolio Context:\n{context}\n\nUser: {message}"

# Chat endpoint 
@app.post("/chat")
async def chat(req: ChatRequest):
    # Short-circuit greetings 
    if is_greeting(req.message):
        return {"response": random.choice(GREETING_RESPONSES)}

    print("CLASSIFY START:", time.time())
    mode = classify_query(req.message)
    print("CLASSIFY END:", time.time())

    context = retrieve_portfolio_context(req.message) if mode == "portfolio" else ""

    if mode == "portfolio" and not has_context(context):
        return {"response": "I don't have enough verified information in the portfolio to answer that."}

    user_content = build_user_content(mode, context, req.message)

    # Streaming response
    def generate():
        try:
            print("LLM STREAM START:", time.time())
            stream = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3",
                messages=[
                    {"role": "system", "content": QUILL_SYSTEM_PROMPT},
                    {"role": "user",   "content": user_content}        # no duplicate prompt
                ],
                temperature=0.7,
                stream=True
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
            print("LLM STREAM END:", time.time())
        except Exception as e:
            print("OPENROUTER ERROR:", e)
            yield "Quill is temporarily unavailable."

    return StreamingResponse(generate(), media_type="text/plain")

# Health check (lets cron-job.org keep Render alive)
@app.get("/")
def health():
    return {"status": "Quill is alive"}