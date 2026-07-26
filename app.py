"""
Phase 4 — Streamlit chat UI.

A chat interface over the RAG pipeline: pick a framework (or search all), ask a
question, and get an answer with clickable source citations.

Run with:
    streamlit run app.py
"""

import os

import streamlit as st

from sources import FRAMEWORKS
from rag import answer, OPENAI_MODEL

st.set_page_config(page_title="AI Dev Docs Assistant", page_icon="🧠", layout="centered")

# Map display names -> framework keys for the sidebar selector.
FRAMEWORK_CHOICES = {"All frameworks": None}
for _key, _cfg in FRAMEWORKS.items():
    FRAMEWORK_CHOICES[_cfg["name"]] = _key


def render_sources(sources):
    if not sources:
        return
    with st.expander(f"📎 {len(sources)} source(s)"):
        for i, s in enumerate(sources, 1):
            st.markdown(f"{i}. [{s['title']}]({s['url']}) &nbsp;·&nbsp; `{s['framework']}`")


# ---- Sidebar ----
with st.sidebar:
    st.header("⚙️ Options")
    choice = st.selectbox(
        "Framework",
        list(FRAMEWORK_CHOICES),
        help="Scope the search to one framework, or search across all of them.",
    )
    framework = FRAMEWORK_CHOICES[choice]
    st.caption(f"Answer model: `{OPENAI_MODEL}`")

    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key == "sk-your-key-here":
        st.warning(
            "No OpenAI key set — add `OPENAI_API_KEY` to `.env` for generated answers. "
            "Retrieval and sources still work without it."
        )

    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ---- Header ----
st.title("🧠 AI Dev Docs Assistant")
st.caption(
    "Ask about LangGraph · LangChain · CrewAI · OpenAI Agents SDK · "
    "Google ADK · FastAPI · Kubernetes. Every answer cites its sources."
)

# ---- Conversation history ----
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            render_sources(msg.get("sources", []))

# ---- Chat input ----
if prompt := st.chat_input("How do I create a conditional edge in LangGraph?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        scope = choice if framework else "all frameworks"
        with st.spinner(f"Searching {scope}…"):
            text, sources = answer(prompt, framework)
        st.markdown(text)
        render_sources(sources)

    st.session_state.messages.append({"role": "assistant", "content": text, "sources": sources})
