# 🔎 AI Custom Search Engine

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![LLM](https://img.shields.io/badge/LLM-OpenAI%20gpt--4o--mini-brightgreen.svg)](https://platform.openai.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](file:///c:/Users/Kavya/Desktop/ai-search-engine/LICENSE)
[![Search](https://img.shields.io/badge/search-DuckDuckGo-lightgrey.svg)]()

A premium, interactive command-line interface (CLI) search engine and research assistant. It integrates concurrent web crawling and OpenAI's GPT LLM to deliver grounded answers with inline source citations.

---

## 🌟 Key Features

*   **📺 Stunning Terminal UI**: Built with the `rich` library, offering gradient banners, progress loaders, formatted tables, markdown rendering, and interactive menus.
*   **⚡ Dual-Mode Search**:
    *   **Fast Search**: Quick retrieval using search snippets. Ideal for quick questions and fast facts (2-3 seconds).
    *   **Deep Search**: Full page crawler. Fetches, cleans, and parses the top 3-5 pages in parallel, converting them to clean Markdown for a deeper, highly-synthesized analysis.
*   **💬 Context-Aware Follow-up Chat**: Start a chat session based directly on search results. Ask follow-up questions or perform deeper synthesis on the gathered sources without re-scraping.
*   **📜 Search History Database**: Offline, persistent JSON history manager. Re-visit previous query summaries, inspect references, or clear historical data.
*   **📄 Markdown Report Exporter**: Instantly export research reports containing queries, synthesized answers, and structured source lists (with URLs and snippets) under `exports/`.
*   **⚙️ Live Configuration Menu**: Adjust the default OpenAI model (e.g., `gpt-4o-mini`, `gpt-4o`) or modify search result limits on the fly.
*   **🛡️ Free Search Engine**: Queries DuckDuckGo for web search results (completely free, no setup or search API keys required).

---

## 📊 Dual-Mode Comparison

| Feature | ⚡ Fast Search | 🔍 Deep Search |
| :--- | :--- | :--- |
| **Data Source** | Search Engine Snippets (Title + Short description) | Full HTML content of top pages (Parallel scrape) |
| **Processing** | Directly parsed and sent to OpenAI | Sanitized (non-content elements like scripts/footers removed) -> Markdown conversion -> Snipped to fit context limits |
| **Response Time** | 2 - 4 Seconds | 5 - 10 Seconds |
| **Best Used For** | Quick lookups, definitions, current dates, simple questions | Deep research, programming bugs, comparative analysis, long articles |

---

## 🚀 Setup Instructions

### 1. Clone & Configure Keys
1. Get an API Key from [OpenAI Platform](https://platform.openai.com/).
2. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and fill in your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

### 2. Install Dependencies
Initialize a virtual environment and install the required packages:

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the CLI
Start the application dashboard:
```bash
python main.py
```

---

## 🛠️ CLI Navigation Guide

When you launch `main.py`, you are presented with the primary dashboard:

### 1. 🔎 AI Search
*   **Query Prompt**: Input your search topic.
*   **Mode Selector**: Choose `fast` or `deep`.
*   **Result Count**: Define how many search engine results to inspect (default: `5`, max: `10`).
*   **Output Actions**:
    *   `1` **Ask Follow-up**: Enters a conversational chat where the LLM retains memory of the web search.
    *   `2` **Export Report**: Saves a detailed `.md` report under the `exports/` folder.
    *   `3` **New Search**: Runs a fresh query.
    *   `4` **Main Menu**: Returns to the home screen.

### 2. 📜 View Search History
*   Displays a list of past queries and execution modes (latest first).
*   Select a record number (e.g., `1`) to view the query details, the full generated answer, and source citations.
*   Type `c` to clear all history, or `m` to return to the main menu.

### 3. ⚙️ Settings & API Status
*   Inspect status checks (configured vs missing keys).
*   Change LLM default model (`gpt-4o-mini`, `gpt-4o`).
*   Change default search limit.

---

## 📖 Example Usage

Here is a live demonstration of running the CLI with a real-time event:

```
Query: who won the austrian grand prix 2026
Mode: FAST

🤖 AI Synthesized Answer

Winner of the 2026 Austrian Grand Prix

The 2026 Austrian Grand Prix was won by George Russell from the Mercedes team. The race took place on June 28, 2026, at the Red Bull Ring in Spielberg, Austria. In a competitive event, Russell secured his victory by successfully holding off Max Verstappen, who finished in second place, 1.6 seconds behind him [2][5]. This win has bolstered Russell's position in the Drivers' Championship standings [2].
```

---

## 📂 Project Architecture

*   [main.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/main.py): Controls CLI main loops, terminal rendering, and the interactive flow.
*   [config.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/config.py): Manages system thresholds, credentials validation, defaults, and LLM model support.
*   [search_client.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/search_client.py): Fetches search listings using the DuckDuckGo (`ddgs`) API.
*   [scraper.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/scraper.py): Resolves HTTP requests in parallel using multithreading. Uses `BeautifulSoup4` to strip templates (nav/footer/styles) and `html2text` for converting HTML to structured markdown.
*   [llm_client.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/llm_client.py): Formats prompt context, implements system rules (like strict grounding and inline citations `[1]`), and holds active chat instances.
*   [utils.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/utils.py): Handles local history storage (JSON) and markdown reports generation.

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](file:///c:/Users/Kavya/Desktop/ai-search-engine/LICENSE) file for details.
