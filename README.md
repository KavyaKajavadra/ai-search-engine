# 🔎 AI Custom Search Engine

A premium, interactive Command-Line Interface (CLI) web search and research assistant powered by Google Gemini and live web crawling. 

This project combines live search queries with Large Language Model (LLM) capabilities to deliver grounded, synthesized answers with source citations. 

**Cost to run: 0 Rupees** (Utilizes free search crawling and Gemini's free tier).

---

## 🌟 Key Features

1. **Stunning Terminal Dashboard**: A visually rich console interface using `rich` for gradients, text formatting, loaders, markdown displays, and panels.
2. **Dual-Mode Research**:
   - ⚡ **Fast Search**: Quick retrieval using search engine snippets. Ideal for quick facts and fast answers (2-3 seconds).
   - 🔍 **Deep Search**: Downloads and scrapes the full content of the top 3-5 pages in parallel, parses HTML into clean Markdown text, and runs deep synthesis. Perfect for detailed topics and complex research.
3. **💬 Interactive Follow-up Chat**: Start a chat session based directly on the retrieved search results. Ask follow-up questions, request deeper analysis, or summarize specific sources without re-searching.
4. **📜 Persistent Search History**: Browse, review, or clear past search results and synthesized answers inside an offline JSON search history database.
5. **📄 Markdown Report Exporter**: Export research findings instantly to clean, structured Markdown reports with citations and sources under the `exports/` folder.
6. **Robust Fallbacks**: Searches DuckDuckGo for free by default (no API keys required), but can optionally use Google Custom Search API if provided.

---

## 🛠️ Tech Stack & Architecture

- **Core**: Python 3.10+
- **LLM Engine**: Google Gemini API via the `google-generativeai` SDK
- **Web Search**: DuckDuckGo API (via `duckduckgo_search`) or optional Google Custom Search API
- **Web Scraping**: `httpx` (HTTP fetching) + `beautifulsoup4` (DOM cleaning) + `html2text` (markdown generation)
- **Visual styling**: `rich` library (spinners, layouts, markdown support)
- **Modular Design**: Exposes decoupled components (`search_client`, `scraper`, `llm_client`) allowing for easy transition to a startup SaaS web backend (like FastAPI/Flask) later.

---

## 🚀 Setup Instructions

### 1. Configure API Keys
1. Get a free API Key from [Google AI Studio](https://aistudio.google.com/).
2. Copy the `.env.example` file and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and paste your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

*Note: Google Custom Search API key is completely optional. If left blank, it will default to DuckDuckGo, which is free and needs no key.*

### 2. Set Up Virtual Environment & Dependencies
Initialize a virtual environment and install the required Python packages:

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Application
Run the main script to open the interactive dashboard:
```bash
python main.py
```

---

## 📂 Project Structure

```
ai-search-engine/
├── .env                  # Private API credentials (not checked into git)
├── .env.example          # Template for environment configuration
├── requirements.txt      # Required libraries (Gemini, bs4, rich, etc.)
├── config.py             # Config center (models, limitations, API validation)
├── search_client.py      # Core search requester (DuckDuckGo/Google)
├── scraper.py            # Concurrent scraper & HTML cleanup parser
├── llm_client.py         # Handles prompt engineering and Gemini generation/chat
├── utils.py              # Exporter & search history controller
├── main.py               # Main CLI app loop & console visual layout
└── exports/              # Directory where generated Markdown reports are saved
```
