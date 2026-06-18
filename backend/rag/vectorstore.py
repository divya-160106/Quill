print("VECTORSTORE FILE LOADED")
import os
import time
import requests
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "quill_portfolio"

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"

print("CURRENT WORKING DIR:", os.getcwd())
print("DB PATH RESOLVED TO:", os.path.abspath(DB_PATH))

#  HF INFERENCE API EMBEDDINGS (no local model load)

class HFInferenceEmbeddings:
    def __init__(self, api_url=HF_MODEL_URL, token=HF_API_TOKEN):
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {token}"}

    def _call_api(self, texts):
        payload = {"inputs": texts, "options": {"wait_for_model": True}}
        for attempt in range(3):
            resp = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                # Some models return token-level vectors; mean-pool if so
                if isinstance(data[0][0], list):
                    return [
                        [sum(dim) / len(dim) for dim in zip(*token_vecs)]
                        for token_vecs in data
                    ]
                return data
            if resp.status_code == 503:
                wait = resp.json().get("estimated_time", 5)
                print(f"Model loading, retrying in {wait}s...")
                time.sleep(min(wait, 15))
                continue
            raise RuntimeError(f"HF API error {resp.status_code}: {resp.text}")
        raise RuntimeError("HF API failed after retries")

    def embed_documents(self, texts):
        return self._call_api(texts)

    def embed_query(self, text):
        return self._call_api([text])[0]

# SINGLETON EMBEDDING

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("USING HF INFERENCE API EMBEDDINGS")
        _embedding_model = HFInferenceEmbeddings()
    return _embedding_model


def get_vectorstore():
    print("CHROMA DB PATH:", DB_PATH)
    print("EXISTS:", os.path.exists(DB_PATH))
    print("COLLECTION NAME:", COLLECTION_NAME)
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=get_embedding_model(),
        collection_name=COLLECTION_NAME
    )