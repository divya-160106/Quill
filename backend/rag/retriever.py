from rag.vectorstore import get_vectorstore

_db = None

def get_db():
    global _db
    if _db is None:
        _db = get_vectorstore()
    return _db

def retrieve_portfolio_context(query: str) -> str:
    db = get_db()
    results = db.similarity_search(query, k=4)  # was 9, 4 is plenty
    return "\n\n".join([r.page_content for r in results])