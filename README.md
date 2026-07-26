# 🧠 AI Engineering Documentation Assistant

A **Retrieval-Augmented Generation (RAG)** assistant that answers questions about popular AI-engineering frameworks — **with source citations** — so developers stop digging through docs.

Ask it _"How do I create a conditional edge in LangGraph?"_ and it retrieves the relevant documentation and answers, linking back to the exact source page.

![The assistant answering a LangGraph question with a cited, syntax-highlighted code example](assets/ui-answer.png)

---

## ✨ Features

- 🔍 **Semantic search** across **829 official documentation pages** (22,453 indexed chunks)
- 💬 **Conversational Q&A** with follow-up questions and chat history
- 📎 **Source citations** on every answer, with framework badges
- 🧩 **Filter by framework** — ask within one, or search all seven at once
- 🧪 **Example prompts** and a live index-stats sidebar
- ⚡ **Free, local embeddings** — the only paid piece is the OpenAI answer call

## 📚 Supported frameworks

**LangGraph · LangChain · OpenAI Agents SDK · Google ADK · CrewAI · FastAPI · Kubernetes**

## 🏗️ How it works

```
Indexing (once):   docs → crawl → chunk → embed → store in ChromaDB
Answering (live):  question → embed → search → relevant docs → OpenAI → cited answer
```

The LLM never answers from memory — it answers only from the documentation retrieved for each question, then cites where every claim came from.

## 🛠️ Tech stack

| Layer         | Tool                                     |
| ------------- | ---------------------------------------- |
| Language / UI | Python · Streamlit                       |
| Crawling      | requests · BeautifulSoup · markdownify   |
| Chunking      | langchain-text-splitters                 |
| Embeddings    | all-MiniLM-L6-v2 (local, free)           |
| Vector DB     | ChromaDB (local, free)                   |
| Generation    | OpenAI (`gpt-4o-mini`)                    |

## ✅ Evaluation

A labelled question set (`eval.py`) scores three things — did retrieval surface the right framework, did the answer cite it, and is the answer grounded in the docs. Current score: **10/10 on all three**.

```bash
python eval.py                  # full run (uses OpenAI)
python eval.py --retrieval-only # free retrieval-only check (no API calls)
```

## 🚀 Getting started

### Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Setup

```bash
# 1. Clone
git clone https://github.com/<your-username>/rag-devdocs-assistant.git
cd rag-devdocs-assistant

# 2. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env            # Windows: Copy-Item .env.example .env
# then edit .env and paste your OpenAI key
```

### Run

```bash
python crawl.py        # 1. download the documentation (all 7 frameworks)
python ingest.py       # 2. build the search index
streamlit run app.py   # 3. launch the app
```

> First-time indexing downloads the docs and a small embedding model, then embeds ~22k chunks — it takes a few minutes. After that, everything runs locally and startup is instant.

## 📁 Project structure

```
.
├── sources.py       # config: which frameworks to crawl + how
├── crawl.py         # download docs      → docs/<framework>/
├── ingest.py        # chunk + embed + store in ChromaDB
├── rag.py           # retrieve + ask the LLM (the core)
├── app.py           # Streamlit chat UI
├── eval.py          # evaluation harness
├── requirements.txt
└── .env.example
```

## 📄 License

Released under the MIT License.
