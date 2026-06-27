from rag.vectorstore import get_vectorstore

_db = None

def get_db():
    global _db
    if _db is None:
        _db = get_vectorstore()
    return _db

def retrieve_portfolio_context(query: str) -> str:
    db = get_db()
    project_triggers = ["project", "built", "made", "app", "application", "work", "portfolio"]
    query_lower = query.lower()
    
    if any(word in query_lower for word in project_triggers):
        project_results = db.similarity_search(
            query,
            k=6,
            filter={"section": "PROJECTS"}  
        )
        general_results = db.similarity_search(query, k=3)
        
        seen = set()
        combined = []
        for r in project_results + general_results:
            if r.page_content not in seen:
                seen.add(r.page_content)
                combined.append(r)
        
        return "\n\n".join([r.page_content for r in combined])
    
    return "\n\n".join([r.page_content for r in db.similarity_search(query, k=6)])