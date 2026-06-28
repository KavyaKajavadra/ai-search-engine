import httpx
from bs4 import BeautifulSoup
import html2text
import concurrent.futures
from typing import List, Dict, Any
import config

class WebScraper:
    """Class to scrape web page contents and convert them to clean text/markdown."""

    def __init__(self):
        self.headers = {
            "User-Agent": config.USER_AGENT
        }
        self.timeout = config.SCRAPE_TIMEOUT
        self.max_chars = config.MAX_CHARS_PER_PAGE

        # Configure html2text converter
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = True  # We already track the main URL
        self.html_converter.ignore_images = True
        self.html_converter.ignore_emphasis = False
        self.html_converter.body_width = 0  # No wrapping

    def scrape_url(self, url: str) -> str:
        """
        Fetches the URL and extracts clean markdown-like text.
        Handles errors gracefully by returning an error description.
        """
        if not url:
            return "No URL provided."

        try:
            # Fetch HTML content
            with httpx.Client(headers=self.headers, timeout=self.timeout, follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                html_content = response.text
            
            # Parse HTML and clean up noise (scripts, styles, navs, headers/footers)
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Remove non-content elements to clean up the page
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
                element.decompose()
            
            # Get cleaned HTML string and convert to clean markdown
            cleaned_html = str(soup)
            markdown_content = self.html_converter.handle(cleaned_html)
            
            # Clean up white spaces
            lines = [line.strip() for line in markdown_content.splitlines()]
            cleaned_text = "\n".join([line for line in lines if line])
            
            # Truncate content to avoid exceeding LLM context budget
            if len(cleaned_text) > self.max_chars:
                cleaned_text = cleaned_text[:self.max_chars] + "\n\n[Content truncated due to length limits...]"
                
            return cleaned_text

        except httpx.HTTPStatusError as e:
            return f"Error: HTTP {e.response.status_code} occurred while trying to load the page."
        except httpx.RequestError as e:
            return f"Error: Network issue or timeout occurred ({e})."
        except Exception as e:
            return f"Error: Failed to parse website content ({e})."

    def scrape_urls_parallel(self, urls: List[str]) -> List[str]:
        """
        Scrapes a list of URLs concurrently using thread pools.
        Maintains order matching the input URL list.
        """
        results = ["" for _ in urls]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls) or 1) as executor:
            # Map scraping task
            future_to_idx = {executor.submit(self.scrape_url, url): i for i, url in enumerate(urls)}
            
            for future in concurrent.futures.as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    results[idx] = f"Error during parallel execution: {e}"
                    
        return results
