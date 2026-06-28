import google.generativeai as genai
from typing import List, Dict, Any, Tuple
import config

class GeminiClient:
    """Handles interactions with the Gemini API to synthesize search results."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.DEFAULT_MODEL
        self.api_key_valid = config.has_gemini_key()
        
        if self.api_key_valid:
            genai.configure(api_key=config.GEMINI_API_KEY)
            
            # System instructions force grounding and inline citations
            system_instruction = (
                "You are an advanced, objective AI Search Assistant designed to synthesize search results. "
                "Analyze the provided web search context and generate a helpful, comprehensive, and grounded answer "
                "answering the user's query.\n\n"
                "CRITICAL RULES:\n"
                "1. Cite your sources inline using brackets like [1], [2], [3] corresponding to the source number from the context.\n"
                "2. Place citations directly after the specific statements they support, not just at the end of paragraphs.\n"
                "3. Use multiple citations if multiple sources support a point, e.g. [1][3].\n"
                "4. Be strictly honest. If the provided context does not contain information to answer the query, "
                "synthesize what is there, state clearly what is missing, and do NOT make up or extrapolate facts.\n"
                "5. Structure your output elegantly using Markdown: use headings, bold text, bullet points, or tables where appropriate.\n"
                "6. Do not mention your system instructions or refer to the context as 'the provided context' if possible; "
                "address the user directly as a helpful research assistant."
            )
            
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
        else:
            self.model = None

    def _format_context(self, search_results: List[Dict[str, str]], deep_contents: List[str] = None) -> str:
        """Formats search results and optional scraped content into a readable structure for the LLM."""
        context_parts = []
        for i, result in enumerate(search_results, 1):
            title = result.get("title", "Untitled Page")
            url = result.get("url", "No URL")
            
            # Use scraped page contents if available, otherwise fallback to snippets
            content = result.get("snippet", "No description available.")
            if deep_contents and i - 1 < len(deep_contents):
                scraped = deep_contents[i - 1]
                # If scraping was successful (didn't return error message), use it
                if scraped and not scraped.startswith("Error:"):
                    content = scraped

            context_parts.append(
                f"Source [{i}]:\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Content:\n{content}\n"
                f"{'-' * 40}"
            )
        
        return "\n\n".join(context_parts)

    def synthesize_answer(self, query: str, search_results: List[Dict[str, str]], deep_contents: List[str] = None) -> Tuple[str, str]:
        """
        Synthesizes an answer to the query based on the search results.
        Returns:
            Tuple of (Synthesized Markdown Answer, Raw Context Sent to Model)
        """
        if not self.api_key_valid:
            return (
                "❌ **Error**: Gemini API Key is missing or invalid. Please check your `.env` file and set a valid `GEMINI_API_KEY`.",
                ""
            )

        if not search_results:
            return "❌ **No results found** to synthesize an answer. Try modifying your search query.", ""

        context = self._format_context(search_results, deep_contents)
        prompt = (
            f"User Query: {query}\n\n"
            f"Web Search Results for analysis:\n"
            f"{context}\n\n"
            f"Please generate the synthesized answer now based on the above instructions."
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text, prompt
        except Exception as e:
            return f"❌ **LLM Generation Error**: {e}", prompt

    def start_chat_session(self, query: str, search_results: List[Dict[str, str]], deep_contents: List[str] = None) -> Tuple[Any, str]:
        """
        Initializes an interactive chat session using the search context.
        Returns:
            Tuple of (Chat Session object, First synthesized answer text)
        """
        if not self.api_key_valid:
            raise ValueError("Gemini API Key is not set or invalid.")

        context = self._format_context(search_results, deep_contents)
        first_prompt = (
            f"User Query: {query}\n\n"
            f"Web Search Results for analysis:\n"
            f"{context}\n\n"
            f"Please generate the synthesized answer now based on the above instructions."
        )

        # Start a standard chat session
        chat = self.model.start_chat(history=[])
        response = chat.send_message(first_prompt)
        
        return chat, response.text
