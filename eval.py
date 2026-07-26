"""
Phase 6 — Evaluation harness.

Runs a small labelled test set through the RAG pipeline and scores three things
per question:
  - retrieval: did we retrieve a chunk from the EXPECTED framework?
  - citation:  did the generated answer cite a source from that framework?
  - keyword:   does the answer mention an expected key term? (a groundedness proxy)

Each question has a known "home" framework, so we can check the system surfaces
and answers from the right docs — without a framework filter.

Usage:
    python eval.py                   # full eval (uses OpenAI)
    python eval.py --retrieval-only  # retrieval scoring only, no OpenAI calls (free)
"""

import sys

from rag import retrieve, answer

EVAL_SET = [
    {"q": "How do I create a conditional edge in LangGraph?",             "fw": "langgraph",  "keywords": ["conditional", "add_conditional_edges"]},
    {"q": "How do I add persistence with a checkpointer in LangGraph?",   "fw": "langgraph",  "keywords": ["checkpoint"]},
    {"q": "How do I call tools with a chat model in LangChain?",          "fw": "langchain",  "keywords": ["tool"]},
    {"q": "How do I create a Crew with multiple agents in CrewAI?",       "fw": "crewai",     "keywords": ["crew", "agent"]},
    {"q": "How do I add guardrails to an agent in the OpenAI Agents SDK?","fw": "openai",     "keywords": ["guardrail"]},
    {"q": "How do agent handoffs work in the OpenAI Agents SDK?",         "fw": "openai",     "keywords": ["handoff"]},
    {"q": "How do I run a background task in FastAPI?",                    "fw": "fastapi",    "keywords": ["background"]},
    {"q": "How do I declare path parameters in FastAPI?",                 "fw": "fastapi",    "keywords": ["path"]},
    {"q": "What is a Deployment in Kubernetes?",                          "fw": "kubernetes", "keywords": ["deployment", "replica"]},
    {"q": "What is a Pod in Kubernetes?",                                 "fw": "kubernetes", "keywords": ["pod", "container"]},
]


def mark(passed):
    return "PASS" if passed else "fail"


def contains_any(text, keywords):
    low = text.lower()
    return any(k.lower() in low for k in keywords)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    retrieval_only = "--retrieval-only" in sys.argv
    n = len(EVAL_SET)
    print(f"Running {n} eval cases{' (retrieval only)' if retrieval_only else ''}...\n")

    r_ok = c_ok = k_ok = 0
    for case in EVAL_SET:
        chunks = retrieve(case["q"], k=5)
        retr = case["fw"] in {c["framework"] for c in chunks}
        r_ok += retr

        if retrieval_only:
            print(f"  [retrieval {mark(retr)}]  ({case['fw']}) {case['q']}")
            continue

        text, sources = answer(case["q"])
        cite = case["fw"] in {s["framework"] for s in sources}
        kw = contains_any(text, case["keywords"])
        c_ok += cite
        k_ok += kw
        print(f"  [retr {mark(retr)} | cite {mark(cite)} | kw {mark(kw)}]  ({case['fw']}) {case['q']}")

    print()
    if retrieval_only:
        print(f"Retrieval: {r_ok}/{n} ({round(100 * r_ok / n)}%)")
    else:
        print(f"Retrieval: {r_ok}/{n} ({round(100 * r_ok / n)}%)  |  "
              f"Citation: {c_ok}/{n} ({round(100 * c_ok / n)}%)  |  "
              f"Keyword: {k_ok}/{n} ({round(100 * k_ok / n)}%)")


if __name__ == "__main__":
    main()
