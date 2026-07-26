"""
Phase 1 — Documentation crawler.

Reads FRAMEWORKS from sources.py, discovers pages via each site's sitemap,
downloads the content (clean Markdown when the site offers it, otherwise by
converting HTML), and saves one file per page under docs/<framework>/ with a
metadata header that ingest.py reads later.

Usage:
    python crawl.py               # crawl every framework
    python crawl.py langgraph     # crawl a single framework
"""

import re
import sys
import time
from pathlib import Path
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_md

from sources import FRAMEWORKS

DOCS_DIR = Path("docs")
HEADERS = {"User-Agent": "rag-devdocs-assistant/0.1 (educational project)"}
REQUEST_TIMEOUT = 30
DELAY_SECONDS = 0.3  # be polite: pause between requests
MIN_CONTENT_CHARS = 100  # skip near-empty pages


def get_sitemap_urls(sitemap_url, path_contains=None):
    """Return the list of page URLs listed in a sitemap.xml."""
    resp = requests.get(sitemap_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    # Sitemaps declare an XML namespace; strip it so tag lookups stay simple.
    xml = re.sub(r'\sxmlns="[^"]+"', "", resp.text, count=1)
    urls = [loc.text.strip() for loc in ElementTree.fromstring(xml).iter("loc") if loc.text]
    if path_contains:
        urls = [u for u in urls if path_contains in u]
    return urls


def fetch_mintlify(url):
    """Mintlify sites serve a clean Markdown version of every page at <url>.md."""
    resp = requests.get(url + ".md", headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    md = resp.text
    md = re.sub(r"^(>.*\n)+\s*", "", md)  # drop the leading "Documentation Index" note
    md = "\n".join(l for l in md.splitlines() if not l.startswith("export const "))
    md = re.sub(r"(```[^\s`]*) theme=\{[^\n]*", r"\1", md)  # tidy code-fence info strings
    return re.sub(r"\n{3,}", "\n\n", md).strip()


def fetch_html(url):
    """Download the HTML page and convert its main content to Markdown."""
    resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    container = None
    for selector in ["article", "main", '[role="main"]', ".md-content", ".markdown", "body"]:
        container = soup.select_one(selector)
        if container:
            break
    md = html_to_md(str(container or soup), heading_style="ATX")
    return re.sub(r"\n{3,}", "\n\n", md).strip()


def title_from_markdown(md, fallback):
    """Use the first H1 as the page title, else fall back to the URL slug."""
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def url_to_filename(url):
    """Turn a page URL into a safe .md filename."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", re.sub(r"^https?://", "", url)).strip("-").lower()
    return (slug or "index")[:120] + ".md"


def crawl_framework(key, config):
    print(f"\n=== {config['name']} ({key}) ===")
    out_dir = DOCS_DIR / key
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        urls = get_sitemap_urls(config["sitemap"], config.get("path_contains"))
    except Exception as e:
        print(f"  ! could not read sitemap ({config['sitemap']}): {e}")
        return

    urls = urls[: config.get("max_pages", 100)]
    print(f"  found {len(urls)} pages to download (method: {config['method']})")

    fetch = fetch_mintlify if config["method"] == "mintlify" else fetch_html
    saved = 0
    for i, url in enumerate(urls, 1):
        try:
            markdown = fetch(url)
            if len(markdown) < MIN_CONTENT_CHARS:
                print(f"  [{i}/{len(urls)}] empty, skipped: {url}")
                continue
            title = title_from_markdown(markdown, url.rstrip("/").split("/")[-1])
            header = f"---\nurl: {url}\ntitle: {title}\nframework: {key}\n---\n\n"
            (out_dir / url_to_filename(url)).write_text(header + markdown, encoding="utf-8")
            saved += 1
            print(f"  [{i}/{len(urls)}] saved: {title[:60]}")
        except Exception as e:
            print(f"  [{i}/{len(urls)}] skipped {url} ({e})")
        time.sleep(DELAY_SECONDS)

    print(f"  done -> {saved} pages saved to {out_dir}/")


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else None
    if which:
        if which not in FRAMEWORKS:
            print(f"Unknown framework '{which}'. Options: {', '.join(FRAMEWORKS)}")
            sys.exit(1)
        crawl_framework(which, FRAMEWORKS[which])
    else:
        for key, config in FRAMEWORKS.items():
            crawl_framework(key, config)


if __name__ == "__main__":
    main()
