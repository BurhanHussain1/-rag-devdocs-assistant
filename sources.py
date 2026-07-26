"""
Configuration for every documentation source the assistant crawls.

Adding a new framework = adding one entry below. Fields:
  - name:           human-readable name (shown later in the UI)
  - method:         how to fetch a page's content:
                      "mintlify" -> fetch the clean `<url>.md` a Mintlify site serves
                      "html"     -> download the HTML page and convert it to Markdown
  - sitemap:        URL of the site's sitemap.xml (used to discover every page)
  - path_contains:  only keep page URLs whose path contains this string
                    (None = keep all). Scopes large or shared doc sites.
  - max_pages:      safety cap on pages downloaded per framework

Confirmed working: langgraph, langchain (both live on docs.langchain.com).
Entries marked "VERIFY" are best-guess configs to test when we enable them.
"""

FRAMEWORKS = {
    "langgraph": {
        "name": "LangGraph",
        "method": "mintlify",
        "sitemap": "https://docs.langchain.com/sitemap.xml",
        "path_contains": "/oss/python/langgraph",
        "max_pages": 150,
    },
    "langchain": {
        "name": "LangChain",
        "method": "mintlify",
        "sitemap": "https://docs.langchain.com/sitemap.xml",
        "path_contains": "/oss/python/langchain",
        "max_pages": 150,
    },
    "crewai": {  # VERIFY — docs.crewai.com is also a Mintlify site
        "name": "CrewAI",
        "method": "mintlify",
        "sitemap": "https://docs.crewai.com/sitemap.xml",
        "path_contains": None,
        "max_pages": 150,
    },
    "google_adk": {  # VERIFY — MkDocs site
        "name": "Google ADK",
        "method": "html",
        "sitemap": "https://google.github.io/adk-docs/sitemap.xml",
        "path_contains": None,
        "max_pages": 150,
    },
    "fastapi": {  # VERIFY — MkDocs Material
        "name": "FastAPI",
        "method": "html",
        "sitemap": "https://fastapi.tiangolo.com/sitemap.xml",
        "path_contains": None,
        "max_pages": 150,
    },
    "openai": {  # VERIFY — platform.openai.com (JS-heavy; may need a different route)
        "name": "OpenAI SDK",
        "method": "html",
        "sitemap": "https://platform.openai.com/sitemap.xml",
        "path_contains": "/docs/",
        "max_pages": 150,
    },
    "kubernetes": {  # VERIFY — huge site; scoped to the Concepts section
        "name": "Kubernetes",
        "method": "html",
        "sitemap": "https://kubernetes.io/sitemap.xml",
        "path_contains": "/docs/concepts/",
        "max_pages": 150,
    },
}
