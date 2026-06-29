# 🔎 AI Custom Search Engine

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![LLM](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash-orange.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](file:///c:/Users/Kavya/Desktop/ai-search-engine/LICENSE)
[![Search](https://img.shields.io/badge/search-DuckDuckGo%20%7C%20Google-lightgrey.svg)]()

A premium, interactive command-line interface (CLI) search engine and research assistant. It integrates concurrent web crawling and Google's Gemini LLM to deliver grounded answers with inline source citations.

> **Cost to run:** **0 Rupees** (Utilizes DuckDuckGo's free API and Gemini's free API tier).

---

## 🌟 Key Features

*   **📺 Stunning Terminal UI**: Built with the `rich` library, offering gradient banners, progress loaders, formatted tables, markdown rendering, and interactive menus.
*   **⚡ Dual-Mode Search**:
    *   **Fast Search**: Quick retrieval using search snippets. Ideal for quick questions and fast facts (2-3 seconds).
    *   **Deep Search**: Full page crawler. Fetches, cleans, and parses the top 3-5 pages in parallel, converting them to clean Markdown for a deeper, highly-synthesized analysis.
*   **💬 Context-Aware Follow-up Chat**: Start a chat session based directly on search results. Ask follow-up questions or perform deeper synthesis on the gathered sources without re-scraping.
*   **📜 Search History Database**: Offline, persistent JSON history manager. Re-visit previous query summaries, inspect references, or clear historical data.
*   **📄 Markdown Report Exporter**: Instantly export research reports containing queries, synthesized answers, and structured source lists (with URLs and snippets) under `exports/`.
*   **⚙️ Live Configuration Menu**: Adjust the default Gemini LLM model (e.g., `gemini-2.0-flash`, `gemini-1.5-pro`) or modify search result limits on the fly.
*   **🛡️ Robust Fallbacks**: Attempts to use Google Custom Search API if configured; otherwise, falls back automatically to DuckDuckGo (completely free, no setup required).

---

## 📊 Dual-Mode Comparison

| Feature | ⚡ Fast Search | 🔍 Deep Search |
| :--- | :--- | :--- |
| **Data Source** | Search Engine Snippets (Title + Short description) | Full HTML content of top pages (Parallel scrape) |
| **Processing** | Directly parsed and sent to Gemini | Sanitized (non-content elements like scripts/footers removed) -> Markdown conversion -> Snipped to fit context limits |
| **Response Time** | 2 - 4 Seconds | 5 - 10 Seconds |
| **Best Used For** | Quick lookups, definitions, current dates, simple questions | Deep research, programming bugs, comparative analysis, long articles |

---

## 🚀 Setup Instructions

### 1. Clone & Configure Keys
1. Get a free API Key from [Google AI Studio](https://aistudio.google.com/).
2. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and fill in your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
   *(Optional)* If you prefer using Google Custom Search, configure `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`. If left blank/commented out, the system will use DuckDuckGo automatically.

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
*   Change LLM default model (`gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`).
*   Change default search limit.

---

## 📂 Project Architecture

*   [main.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/main.py): Controls CLI main loops, terminal rendering, and the interactive flow.
*   [config.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/config.py): Manages system thresholds, credentials validation, defaults, and LLM model support.
*   [search_client.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/search_client.py): Fetches search listings using the DuckDuckGo (`ddgs`) or Google Custom Search APIs.
*   [scraper.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/scraper.py): Resolves HTTP requests in parallel using multithreading. Uses `BeautifulSoup4` to strip templates (nav/footer/styles) and `html2text` for converting HTML to structured markdown.
*   [llm_client.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/llm_client.py): Formats prompt context, implements system rules (like strict grounding and inline citations `[1]`), and holds active chat instances.
*   [utils.py](file:///c:/Users/Kavya/Desktop/ai-search-engine/utils.py): Handles local history storage (JSON) and markdown reports generation.

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](file:///c:/Users/Kavya/Desktop/ai-search-engine/LICENSE) file for details.
