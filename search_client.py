import httpx
from typing import List, Dict, Any
from ddgs import DDGS
import config

class SearchClient:
    """Class to manage interactions with web search engines (DuckDuckGo and Google Custom Search)."""

    def __init__(self):
        self.use_google = config.has_google_search_keys()
        self.google_api_key = config.GOOGLE_API_KEY
        self.google_cse_id = config.GOOGLE_CSE_ID

    def search(self, query: str, num_results: int = config.DEFAULT_SEARCH_LIMIT) -> List[Dict[str, str]]:
        """
        Executes a web search for the query and returns a normalized list of results.
        Returns:
            List of Dicts, e.g. [{'title': '...', 'url': '...', 'snippet': '...'}]
        """
        if self.use_google:
            try:
                return self._search_google(query, num_results)
            except Exception as e:
                # If Google search fails (e.g. rate limit, bad keys), fallback to DuckDuckGo
                # print(f"Google search failed ({e}). Falling back to DuckDuckGo...") # Log or handle internally
                return self._search_ddg(query, num_results)
        else:
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
            # Let it propagate or return empty list
            raise RuntimeError(f"DuckDuckGo search error: {e}")
            
        return normalized_results

    def _search_google(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """Queries Google Custom Search JSON API."""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.google_api_key,
            "cx": self.google_cse_id,
            "q": query,
            "num": num_results
        }
        
        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        normalized_results = []
        items = data.get("items", [])
        for item in items:
            normalized_results.append({
                "title": item.get("title", "Untitled Page"),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
            
        return normalized_results
