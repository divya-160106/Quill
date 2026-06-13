from rag.vectorstore import get_vectorstore

def retrieve_portfolio_context(query: str):
    db = get_vectorstore()

    print("DB INSTANCE:", id(db))
    print("QUERY:", query)

    results = db.similarity_search(query, k=9)

    print("RESULTS COUNT:", len(results))

    for r in results:
        print("----")
        print(r.page_content[:200])

    return "\n\n".join([r.page_content for r in results])