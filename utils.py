import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any
import config

def save_to_history(query: str, mode: str, answer: str, search_results: List[Dict[str, str]]):
    """Saves a search query, its mode, answer, and sources to the local history file."""
    history_file = config.HISTORY_FILE
    
    # Extract only necessary source fields to save space
    sources = []
    for r in search_results:
        sources.append({
            "title": r.get("title", ""),
            "url": r.get("url", "")
        })

    new_record = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "mode": mode,
        "answer": answer,
        "sources": sources
    }

    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
        except Exception:
            history = []

    # Prepend new record to see latest first
    history.insert(0, new_record)
    
    # Cap history at 50 entries
    history = history[:50]

    try:
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving history: {e}")

def load_history() -> List[Dict[str, Any]]:
    """Loads search history records."""
    history_file = config.HISTORY_FILE
    if not os.path.exists(history_file):
        return []
        
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def clear_history():
    """Clears all records in the search history."""
    history_file = config.HISTORY_FILE
    if os.path.exists(history_file):
        try:
            os.remove(history_file)
        except Exception as e:
            print(f"Error clearing history: {e}")

def sanitize_filename(name: str) -> str:
    """Sanitizes strings for safe file naming."""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace(" ", "_").lower()
    return name[:50]

def export_report(query: str, mode: str, answer: str, search_results: List[Dict[str, str]]) -> str:
    """
    Exports the search query, answer, and sources into a structured Markdown document.
    Returns:
        The file path where the report was exported.
    """
    export_dir = "exports"
    os.makedirs(export_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = sanitize_filename(query)
    filename = f"report_{safe_query}_{timestamp}.md"
    file_path = os.path.join(export_dir, filename)

    markdown_lines = [
        f"# AI Search Engine Report: {query}",
        f"\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Search Mode:** {mode.capitalize()} Search  ",
        "\n## Synthesized Answer\n",
        answer,
        "\n## Sources & Citations\n"
    ]

    for i, source in enumerate(search_results, 1):
        title = source.get("title", "Untitled Page")
        url = source.get("url", "")
        snippet = source.get("snippet", "")
        
        markdown_lines.append(f"### [{i}] {title}")
        if url:
            markdown_lines.append(f"- **URL:** [{url}]({url})")
        if snippet:
            markdown_lines.append(f"- **Summary:** *{snippet}*")
        markdown_lines.append("")  # Empty line separator

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_lines))
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to export report: {e}")
