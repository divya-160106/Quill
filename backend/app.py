from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from router import classify_query
from prompts import QUILL_SYSTEM_PROMPT
from rag.retriever import retrieve_portfolio_context
from fastapi.middleware.cors import CORSMiddleware
from llm import client

load_dotenv()

def has_context(context: str):
    return context and len(context.strip()) > 30

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
        "https://quill-aiagent.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

# CHAT ENDPOINT
@app.post("/chat")
def chat(req: ChatRequest):

    mode = classify_query(req.message)

    context = ""

    if mode == "portfolio":
        context = retrieve_portfolio_context(req.message)

    print("USER:", req.message)
    print("MODE:", mode)
    print("CONTEXT:", context)

    if mode == "portfolio" and not has_context(context):
        return {
            "response": "I don't have enough verified information in the portfolio to answer that."
        }

    prompt = f"""
{QUILL_SYSTEM_PROMPT}

Mode: {mode}

Portfolio Context:
{context}

User:
{req.message}
"""

    try:

        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3",
            messages=[
                {
                    "role": "system",
                    "content": QUILL_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:

        print("OPENROUTER ERROR:")
        print(e)

        return {
            "response": "Quill is temporarily unavailable."
        }
