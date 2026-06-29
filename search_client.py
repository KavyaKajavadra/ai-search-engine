from typing import List, Dict
from ddgs import DDGS
import config

class SearchClient:
    """Class to manage interactions with the DuckDuckGo search engine."""

    def __init__(self):
        pass

    def search(self, query: str, num_results: int = config.DEFAULT_SEARCH_LIMIT) -> List[Dict[str, str]]:
        """
        Executes a web search for the query and returns a normalized list of results.
        Returns:
            List of Dicts, e.g. [{'title': '...', 'url': '...', 'snippet': '...'}]
        """
        return self._search_ddg(query, num_results)

    def _search_ddg(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """Queries DuckDuckGo search (free, no API key)."""
        normalized_results = []
        try:
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(query, max_results=num_results))
                
                for r in ddg_results:
                    normalized_results.append({
                        "title": r.get("title", "Untitled Page"),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", "")
                    })
        except Exception as e:
            raise RuntimeError(f"DuckDuckGo search error: {e}")
            
        return normalized_results
