"""
Phase 4/5 — Streamlit chat UI.

A polished chat interface over the RAG pipeline: pick a framework (or search
all), ask a question, and get an answer with clickable source citations.
Code blocks in answers get a copy button automatically (Streamlit built-in).

Run with:
    streamlit run app.py
"""

import os

import streamlit as st

from sources import FRAMEWORKS
from rag import answer, stats, OPENAI_MODEL

st.set_page_config(page_title="AI Dev Docs Assistant", page_icon="🧠", layout="centered")

# Display name + emoji per framework key (for selector and source badges).
FRAMEWORK_META = {
    "langgraph":  ("LangGraph", "🕸️"),
    "langchain":  ("LangChain", "🔗"),
    "crewai":     ("CrewAI", "🚢"),
    "openai":     ("OpenAI Agents", "🤖"),
    "google_adk": ("Google ADK", "🔷"),
    "fastapi":    ("FastAPI", "⚡"),
    "kubernetes": ("Kubernetes", "☸️"),
}

EXAMPLES = [
    "How do I create a conditional edge in LangGraph?",
    "How do I define a Crew with multiple agents in CrewAI?",
    "How do I add guardrails in the OpenAI Agents SDK?",
    "How do I run a background task in FastAPI?",
    "What is a Kubernetes Deployment?",
]


def fw_label(key):
    name, emoji = FRAMEWORK_META.get(key, (FRAMEWORKS.get(key, {}).get("name", key), "📄"))
    return f"{emoji} {name}"


# Sidebar selector: "All frameworks" + one entry per framework.
CHOICES = {"🌐 All frameworks": None}
for _key in FRAMEWORKS:
    CHOICES[fw_label(_key)] = _key


@st.cache_data(show_spinner=False)
def get_stats():
    try:
        return stats()
    except Exception:
        return 0, {}


def render_sources(sources):
    if not sources:
        return
    with st.expander(f"📎 {len(sources)} source(s)"):
        for i, s in enumerate(sources, 1):
            st.markdown(f"{i}. [{s['title']}]({s['url']}) — {fw_label(s['framework'])}")


# ---- session state ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- sidebar ----
with st.sidebar:
    st.header("⚙️ Options")
    choice = st.selectbox("Framework", list(CHOICES), help="Scope the search to one framework, or search all.")
    framework = CHOICES[choice]

    st.caption(f"Answer model: `{OPENAI_MODEL}`")
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key == "sk-your-key-here":
        st.warning("No OpenAI key — add `OPENAI_API_KEY` to `.env` for generated answers. Retrieval still works.")

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    total, counts = get_stats()
    st.caption(f"**Index:** {total:,} chunks")
    for _key in FRAMEWORKS:
        if _key in counts:
            st.caption(f"{fw_label(_key)} · {counts[_key]:,}")

# ---- header ----
st.title("🧠 AI Dev Docs Assistant")
st.caption("Ask about 7 AI-engineering frameworks. Every answer cites its sources.")

# ---- conversation history ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            render_sources(msg.get("sources", []))

# ---- empty-state example questions ----
if not st.session_state.messages:
    st.markdown("**Try an example:**")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex
            st.rerun()

# ---- input handling ----
user_q = st.chat_input("Ask a question about the docs…")
if not user_q and "pending" in st.session_state:
    user_q = st.session_state.pop("pending")

if user_q:
    st.session_state.messages.append({"role": "user", "content": user_q})
    scope = "all frameworks" if framework is None else fw_label(framework)
    with st.spinner(f"Searching {scope}…"):
        text, sources = answer(user_q, framework)
    st.session_state.messages.append({"role": "assistant", "content": text, "sources": sources})
    st.rerun()
