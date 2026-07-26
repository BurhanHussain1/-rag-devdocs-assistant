"""
Configuration for every documentation source the assistant crawls.

Adding a new framework = adding one entry below. Fields:
  - name:           human-readable name (shown later in the UI)
  - method:         how to fetch a page's content:
                      "mintlify" -> fetch the clean `<url>.md` a Mintlify site serves
                      "html"     -> download the HTML page and convert it to Markdown
  - sitemap:        URL of the site's sitemap.xml (crawl.py recurses into
                    sitemap-index files automatically)
  - path_contains:  keep only page URLs containing this string (None = keep all).
                    Scopes large or shared doc sites to the pages we want.
  - path_excludes:  (optional) drop any URL containing one of these strings.
  - url_fix:        (optional) ("old_prefix", "new_prefix") to repair sitemaps
                    generated with a broken base URL.
  - max_pages:      safety cap on pages downloaded per framework.
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
    "crewai": {
        "name": "CrewAI",
        "method": "mintlify",
        "sitemap": "https://docs.crewai.com/sitemap.xml",
        "path_contains": "/edge/en/",  # latest English docs (site ships every version x locale)
        "max_pages": 150,
    },
    "openai": {
        "name": "OpenAI Agents SDK",
        "method": "html",
        "sitemap": "https://openai.github.io/openai-agents-python/sitemap.xml",
        # This sitemap was built with a broken base URL — every <loc> starts with
        # the literal string "None". Repair it to the real site root.
        "url_fix": ("None", "https://openai.github.io/openai-agents-python/"),
        "path_excludes": ["/ja/"],  # drop Japanese translation pages
        "max_pages": 150,
    },
    "google_adk": {
        "name": "Google ADK",
        "method": "html",
        "sitemap": "https://adk.dev/sitemap.xml",  # docs moved here from google.github.io
        "path_excludes": ["/_includes/"],  # drop homepage partial-include fragments
        "max_pages": 150,
    },
    "fastapi": {
        "name": "FastAPI",
        "method": "html",
        "sitemap": "https://fastapi.tiangolo.com/sitemap.xml",
        "path_contains": None,
        "max_pages": 150,
    },
    "kubernetes": {
        "name": "Kubernetes",
        "method": "html",
        "sitemap": "https://kubernetes.io/sitemap.xml",  # a sitemap-index of 17 sub-sitemaps
        "path_contains": "kubernetes.io/docs/concepts/",  # English Concepts section only
        "max_pages": 150,
    },
}
