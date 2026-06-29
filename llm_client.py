import httpx
from typing import List, Dict, Any, Tuple
import config

class OpenAIChatSession:
    """Manages chat session history and follow-up generation for OpenAI GPT models."""

    def __init__(self, model_name: str, system_instruction: str, api_key: str, initial_prompt: str, first_response: str):
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.api_key = api_key
        # Maintain history in standard chat completion structure
        self.messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": initial_prompt},
            {"role": "assistant", "content": first_response}
        ]

    def send_message(self, message_text: str) -> Any:
        """Sends a follow-up message to OpenAI and returns a response wrapper containing text."""
        self.messages.append({"role": "user", "content": message_text})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": self.messages
        }
        
        response = httpx.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        res_data = response.json()
        ans_text = res_data["choices"][0]["message"]["content"]
        
        self.messages.append({"role": "assistant", "content": ans_text})
        
        # Emulate the Response object having a .text property
        class OpenAIResponse:
            def __init__(self, text):
                self.text = text
        return OpenAIResponse(ans_text)

class OpenAIClient:
    """Handles interactions with the OpenAI API to synthesize search results."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.DEFAULT_MODEL
        self.api_key_valid = config.has_openai_key()
        self.openai_key = config.OPENAI_API_KEY
        
        # System instructions force grounding and inline citations
        self.system_instruction = (
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
                "❌ **Error**: OPENAI_API_KEY is missing or invalid. Please check your `.env` file and configure it.",
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
            headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": prompt}
                ]
            }
            response = httpx.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            res_data = response.json()
            answer = res_data["choices"][0]["message"]["content"]
            return answer, prompt
        except Exception as e:
            return f"❌ **OpenAI Generation Error**: {e}", prompt

    def start_chat_session(self, query: str, search_results: List[Dict[str, str]], deep_contents: List[str] = None) -> Tuple[Any, str]:
        """
        Initializes an interactive chat session using the search context.
        Returns:
            Tuple of (Chat Session object, First synthesized answer text)
        """
        if not self.api_key_valid:
            raise ValueError("OPENAI_API_KEY is not set or invalid.")

        context = self._format_context(search_results, deep_contents)
        first_prompt = (
            f"User Query: {query}\n\n"
            f"Web Search Results for analysis:\n"
            f"{context}\n\n"
            f"Please generate the synthesized answer now based on the above instructions."
        )

        try:
            headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": first_prompt}
                ]
            }
            response = httpx.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            res_data = response.json()
            first_answer = res_data["choices"][0]["message"]["content"]
            
            chat = OpenAIChatSession(
                model_name=self.model_name,
                system_instruction=self.system_instruction,
                api_key=self.openai_key,
                initial_prompt=first_prompt,
                first_response=first_answer
            )
            return chat, first_answer
        except Exception as e:
            raise RuntimeError(f"OpenAI Chat Initialization Error: {e}")
