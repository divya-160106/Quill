print("VECTORSTORE FILE LOADED")
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
DB_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "quill_portfolio"

print("CURRENT WORKING DIR:", os.getcwd())
print("DB PATH RESOLVED TO:", os.path.abspath(DB_PATH))

# LOCAL EMBEDDINGS VIA FASTEMBED (ONNX runtime — no torch, much lighter on RAM)

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("LOADING FASTEMBED MODEL (all-MiniLM-L6-v2)...")
        _embedding_model = FastEmbedEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("FASTEMBED MODEL LOADED")
    return _embedding_model


# SINGLETON VECTORSTORE (avoids reopening the Chroma DB from disk every call)

_vectorstore = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        print("CHROMA DB PATH:", DB_PATH)
        print("EXISTS:", os.path.exists(DB_PATH))
        print("COLLECTION NAME:", COLLECTION_NAME)
        _vectorstore = Chroma(
            persist_directory=DB_PATH,
            embedding_function=get_embedding_model(),
            collection_name=COLLECTION_NAME
        )
    return _vectorstore