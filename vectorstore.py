"""
Lightweight, crash-proof local vector store (brute-force cosine search).

Why not a background-indexed DB here: an interrupted write can corrupt an
on-disk ANN index. This store keeps one plain file per framework under
vector_store/ and searches by exact cosine similarity — nothing to corrupt, and
a killed ingest just re-runs that one framework. Exact brute-force over ~22k
384-dim vectors takes only a few milliseconds, which is plenty for this app.

Layout (per framework):
    vector_store/<framework>.npy     float32 matrix [n_chunks, dim], L2-normalized
    vector_store/<framework>.jsonl   one record per line: {id, text, framework, url, title}
"""

import json
from pathlib import Path

import numpy as np

STORE_DIR = Path("vector_store")


def _paths(framework):
    return STORE_DIR / f"{framework}.npy", STORE_DIR / f"{framework}.jsonl"


def framework_done(framework):
    vec_path, rec_path = _paths(framework)
    return vec_path.exists() and rec_path.exists()


def save_framework(framework, embeddings, records):
    """Persist one framework's vectors + records atomically (write temp, rename)."""
    STORE_DIR.mkdir(exist_ok=True)
    vec_path, rec_path = _paths(framework)

    arr = np.asarray(embeddings, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    arr = arr / norms  # normalize so a dot product == cosine similarity

    tmp_vec = vec_path.with_suffix(".npy.tmp")
    tmp_rec = rec_path.with_suffix(".jsonl.tmp")
    np.save(tmp_vec, arr)
    with open(tmp_rec, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp_vec.replace(vec_path)
    tmp_rec.replace(rec_path)


def load_all(only=None):
    """Load (vectors, records) for all frameworks (or just one)."""
    vecs, recs = [], []
    if STORE_DIR.exists():
        for vec_path in sorted(STORE_DIR.glob("*.npy")):
            framework = vec_path.stem
            if only and framework != only:
                continue
            rec_path = vec_path.with_suffix(".jsonl")
            if not rec_path.exists():
                continue
            v = np.load(vec_path)
            with open(rec_path, encoding="utf-8") as f:
                r = [json.loads(line) for line in f]
            if len(r) == len(v):  # guard against a partial write
                vecs.append(v)
                recs.extend(r)
    if not vecs:
        return np.zeros((0, 384), dtype=np.float32), []
    return np.vstack(vecs), recs


def counts():
    """Return {framework: n_chunks} for what's currently stored."""
    out = {}
    if STORE_DIR.exists():
        for rec_path in sorted(STORE_DIR.glob("*.jsonl")):
            with open(rec_path, encoding="utf-8") as f:
                out[rec_path.stem] = sum(1 for _ in f)
    return out


def search(query_embedding, n_results=4, framework=None, _cache={}):
    """Return the top-n records by cosine similarity, optionally one framework."""
    key = framework or "__all__"
    if key not in _cache:
        _cache[key] = load_all(only=framework)
    vectors, records = _cache[key]
    if len(records) == 0:
        return []
    q = np.asarray(query_embedding, dtype=np.float32)
    q = q / (np.linalg.norm(q) or 1.0)
    sims = vectors @ q
    top = np.argsort(-sims)[:n_results]
    return [{**records[i], "score": float(sims[i])} for i in top]
