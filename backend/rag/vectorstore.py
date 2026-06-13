print("VECTORSTORE FILE LOADED")

import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "quill_portfolio"

print("CURRENT WORKING DIR:", os.getcwd())
print("DB PATH RESOLVED TO:", os.path.abspath(DB_PATH))

# =========================
# ✅ SINGLETON EMBEDDING
# =========================
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("LOADING EMBEDDING MODEL (ONCE)")
        _embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    return _embedding_model


# =========================
# VECTOR DB
# =========================
def get_vectorstore():
    print("CHROMA DB PATH:", DB_PATH)
    print("EXISTS:", os.path.exists(DB_PATH))
    print("COLLECTION NAME:", COLLECTION_NAME)

    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=get_embedding_model(),
        collection_name=COLLECTION_NAME
    )