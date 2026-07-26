"""
Phase 3 — Retrieval-Augmented Generation core.

Given a question, retrieve the most relevant documentation chunks from ChromaDB
(optionally scoped to a single framework), then ask OpenAI to answer using ONLY
that context, returning the answer plus numbered source citations.

The `answer()` function is imported by the Streamlit app in Phase 4.

Usage (CLI):
    python rag.py "How do I create a conditional edge in LangGraph?"
    python rag.py -f crewai "How do I create a crew?"
"""

import os

# Quiet ChromaDB telemetry before it is imported (avoids a background reporter).
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import argparse

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "devdocs"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TOP_K = 5

# MUST match the embedding model used in ingest.py, or query vectors won't be
# comparable to the stored ones.
EMBED_FN = embedding_functions.DefaultEmbeddingFunction()

SYSTEM_PROMPT = """You are a documentation assistant for AI-engineering frameworks \
(LangGraph, LangChain, CrewAI, the OpenAI Agents SDK, Google ADK, FastAPI, Kubernetes).

Answer the user's question using ONLY the documentation context provided. Rules:
- If the context does not contain the answer, say so plainly. Never invent APIs or parameters.
- Prefer concrete code examples drawn from the context when they help.
- Cite sources inline as [n], matching the numbered sources in the context.
- Be practical and concise."""


_collection = None


def get_collection():
    """Open the ChromaDB collection once and reuse it across queries."""
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION_NAME, embedding_function=EMBED_FN)
    return _collection


def retrieve(question, framework=None, k=TOP_K):
    """Return the top-k most relevant chunks, optionally scoped to a framework."""
    where = {"framework": framework} if framework else None
    res = get_collection().query(query_texts=[question], n_results=k, where=where)
    chunks = []
    for doc, md, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        chunks.append({
            "text": doc,
            "url": md.get("url", ""),
            "title": md.get("title", ""),
            "framework": md.get("framework", ""),
            "distance": dist,
        })
    return chunks


def unique_sources(chunks):
    """Ordered, de-duplicated list of sources (one per URL) for citation."""
    seen, sources = set(), []
    for c in chunks:
        if c["url"] not in seen:
            seen.add(c["url"])
            sources.append({"url": c["url"], "title": c["title"], "framework": c["framework"]})
    return sources


def build_context(chunks, sources):
    number = {s["url"]: i + 1 for i, s in enumerate(sources)}
    blocks = [f"[{number[c['url']]}] {c['framework']} — {c['title']}\n{c['text']}" for c in chunks]
    return "\n\n---\n\n".join(blocks)


def answer(question, framework=None, k=TOP_K):
    """Retrieve context and generate a cited answer. Returns (answer_text, sources)."""
    chunks = retrieve(question, framework, k)
    if not chunks:
        return "No relevant documentation found in the index.", []

    sources = unique_sources(chunks)

    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key == "sk-your-key-here":
        return ("[No OPENAI_API_KEY found in .env - showing retrieved sources only. "
                "Add your OpenAI key to .env to get generated answers.]", sources)

    context = build_context(chunks, sources)
    client = OpenAI()
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {question}\n\nDocumentation context:\n\n{context}"},
        ],
    )
    return resp.choices[0].message.content, sources


def stats():
    """Return (total_chunks, {framework: count}) for the index — used by the UI."""
    collection = get_collection()
    got = collection.get(include=["metadatas"])
    counts = {}
    for m in got["metadatas"]:
        counts[m["framework"]] = counts.get(m["framework"], 0) + 1
    return collection.count(), counts


def main():
    parser = argparse.ArgumentParser(description="Ask the documentation assistant.")
    parser.add_argument("question", nargs="+", help="Your question")
    parser.add_argument("-f", "--framework", default=None, help="Limit search to one framework")
    args = parser.parse_args()

    text, sources = answer(" ".join(args.question), args.framework)

    print("\n" + "=" * 72)
    print(text)
    print("=" * 72)
    if sources:
        print("\nSources:")
        for i, s in enumerate(sources, 1):
            print(f"  [{i}] ({s['framework']}) {s['title']}")
            print(f"      {s['url']}")


if __name__ == "__main__":
    main()
