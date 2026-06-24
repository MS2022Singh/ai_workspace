"""
Optional, OFF BY DEFAULT web search used only by the Researcher, Analyst,
Economist, and Scientist roles, and only when the person explicitly turns
on "Allow live web research" in Settings. This is the one part of the app
that intentionally sends something to the internet beyond localhost: the
search query text for that specific step (not the whole task, not any
files). Everything else in the app stays fully local regardless of this
setting.
"""
import requests

SEARCH_URL = "https://html.duckduckgo.com/html/"


def search_web(query: str, max_results: int = 4):
    """Best-effort web search. Returns [] on any failure rather than raising,
    so a flaky network never breaks the task pipeline."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return []

    try:
        r = requests.post(
            SEARCH_URL,
            data={"q": query},
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0 (AI Workspace local app)"},
        )
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for result in soup.select(".result")[:max_results]:
            title_el = result.select_one(".result__title a") or result.select_one("a.result__a")
            snippet_el = result.select_one(".result__snippet")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            url = title_el.get("href", "")
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            if title:
                results.append({"title": title, "url": url, "snippet": snippet})
        return results
    except Exception:
        return []
