"""
Phase 2 — Ingestion pipeline.

Reads crawled pages under docs/<framework>/, splits each into overlapping,
Markdown-aware chunks, and stores them in a local ChromaDB vector store with
metadata (framework / url / title) so Phase 3 can retrieve and filter by
framework.

Embeddings run locally and free via ChromaDB's built-in model
(all-MiniLM-L6-v2) — no API key or per-call cost.

Chunks are upserted file-by-file (low memory, resumable — re-running is safe
because ids are stable and upsert overwrites).

Usage:
    python ingest.py              # ingest every framework
    python ingest.py langgraph    # ingest a single framework
    python ingest.py --reset      # wipe the whole collection first, then ingest all
"""

import re
import sys
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = Path("docs")
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "devdocs"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# Local, free embedding model (all-MiniLM-L6-v2). Phase 3 must use the same one.
# To upgrade quality later (Phase 5): pip install sentence-transformers, then
#   EMBED_FN = embedding_functions.SentenceTransformerEmbeddingFunction("BAAI/bge-base-en-v1.5")
EMBED_FN = embedding_functions.DefaultEmbeddingFunction()

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_document(path):
    """Split a crawled file into (metadata dict, body markdown)."""
    text = path.read_text(encoding="utf-8")
    meta = {"framework": path.parent.name, "url": "", "title": path.stem}
    m = FRONT_MATTER.match(text)
    body = text
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
        body = text[m.end():]
    return meta, body.strip()


def build_splitter():
    """Markdown-aware splitter: prefer breaking at headings, then paragraphs."""
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""],
    )


def main():
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    only = names[0] if names else None

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    if "--reset" in flags and only is None:
        try:
            client.delete_collection(COLLECTION_NAME)
            print("reset: deleted existing collection", flush=True)
        except Exception:
            pass
    collection = client.get_or_create_collection(COLLECTION_NAME, embedding_function=EMBED_FN)

    files = sorted((DOCS_DIR / only).glob("*.md")) if only else sorted(DOCS_DIR.rglob("*.md"))
    if not files:
        print("No docs found. Run crawl.py first.", flush=True)
        return

    label = f" for '{only}'" if only else ""
    print(f"Ingesting {len(files)} files{label}...", flush=True)

    # Resume by default: skip files already ingested (so a killed run can just
    # be re-run until complete). Pass --force (per framework) or --reset (all)
    # to re-embed everything.
    resume = "--reset" not in flags and "--force" not in flags
    total = skipped = failed = 0
    for n, path in enumerate(files, 1):
        meta, body = parse_document(path)
        framework = meta.get("framework", "unknown")
        first_id = f"{framework}--{path.stem}--0"
        if resume and collection.get(ids=[first_id])["ids"]:
            skipped += 1
            print(f"  [{n}/{len(files)}] {framework}: {path.stem[-40:]}  (skip, done)", flush=True)
            continue
        try:
            chunks = build_splitter().split_text(body)
            if chunks:
                collection.upsert(
                    ids=[f"{framework}--{path.stem}--{i}" for i in range(len(chunks))],
                    documents=chunks,
                    metadatas=[
                        {"framework": framework, "url": meta.get("url", ""), "title": meta.get("title", "")}
                        for _ in chunks
                    ],
                )
                total += len(chunks)
            print(f"  [{n}/{len(files)}] {framework}: {path.stem[-40:]}  (+{len(chunks)}, {total} total)", flush=True)
        except Exception as e:
            failed += 1
            print(f"  [{n}/{len(files)}] {framework}: {path.stem[-40:]}  FAILED ({type(e).__name__}); skipping", flush=True)

    print(f"\nDone{label}. +{total} new chunks, {skipped} skipped, {failed} failed. "
          f"Collection holds {collection.count()} chunks.", flush=True)


if __name__ == "__main__":
    main()
