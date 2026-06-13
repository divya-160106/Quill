import os
from rag.vectorstore import get_vectorstore
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(BASE_DIR, "portfolio_docs")


def load_docs():
    docs = []

    if not os.path.exists(DOC_PATH):
        os.makedirs(DOC_PATH)
        return docs

    for file in os.listdir(DOC_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DOC_PATH, file), "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    docs.append(content)

    return docs


def split_sections(text):
    sections = {}
    current = "GENERAL"
    buffer = []

    lines = text.split("\n")

    for line in lines:
        stripped = line.strip()

        # detect section headers (more flexible than only uppercase)
        is_header = (
            stripped.isupper()
            and 2 <= len(stripped) <= 40
            and not stripped.endswith(":")
        )

        if is_header:
            # save previous section
            if buffer:
                sections[current] = "\n".join(buffer).strip()

            current = stripped
            buffer = []
        else:
            buffer.append(line)

    # final section
    if buffer:
        sections[current] = "\n".join(buffer).strip()

    # remove empty sections
    sections = {k: v for k, v in sections.items() if v and len(v) > 5}

    return sections


def ingest():
    raw_docs = load_docs()
    db = get_vectorstore()
    total = 0

    for doc in raw_docs:
        sections = split_sections(doc)

        for section, content in sections.items():
            if len(content.strip()) < 20:
                continue

            db.add_texts(
                texts=[content],
                metadatas=[{
                    "section": section,
                    "length": len(content),
                    "type": "portfolio"
                }]
            )

            total += 1

    print(f"Ingestion complete! Indexed {total} sections.")


if __name__ == "__main__":
    ingest()