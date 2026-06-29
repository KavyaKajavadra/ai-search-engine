import sys
import os
import warnings
# Suppress deprecation and future warnings for a clean CLI output
warnings.filterwarnings("ignore")
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt, IntPrompt, Confirm

import config
from search_client import SearchClient
from scraper import WebScraper
from llm_client import OpenAIClient
import utils

# Initialize rich console for beautiful outputs
console = Console()

def clear_terminal():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def print_welcome_banner():
    """Prints the welcome banner with nice colors and styles."""
    clear_terminal()
    banner_text = Text()
    banner_text.append("🔎 AI CUSTOM SEARCH ENGINE 🔎\n", style="bold cyan")
    banner_text.append("A Premium RAG Tool Built with OpenAI & Live Web Scraping\n", style="dim white")
    banner_text.append(f"Model: {config.DEFAULT_MODEL}  |  Search: DuckDuckGo (Free)", style="italic green")
    
    console.print(
        Panel(
            Align.center(banner_text),
            border_style="bold cyan",
            title="[bold white]v1.0[/bold white]",
            subtitle="[dim]Costs: 0 Rupees[/dim]"
        )
    )
    # Check if OpenAI key is available; warn user if not.
    config.print_setup_warning()

def run_ai_search(search_client: SearchClient, scraper: WebScraper):
    """Executes a new AI search workflow."""
    print_welcome_banner()
    
    # Check if we have the OpenAI key
    if not config.has_openai_key():
        console.print("[bold red]Error:[/] You must set your `OPENAI_API_KEY` in the `.env` file to use the AI capabilities.")
        input("\nPress Enter to return to the main menu...")
        return

    # 1. Get query
    query = Prompt.ask("\n[bold yellow]Enter your search query[/]")
    if not query.strip():
        console.print("[red]Query cannot be empty.[/]")
        input("\nPress Enter to return...")
        return

    # 2. Get mode
    mode = Prompt.ask(
        "[bold yellow]Select Search Mode[/]",
        choices=["fast", "deep"],
        default="fast"
    )

    # 3. Get results limit
    limit = IntPrompt.ask(
        "[bold yellow]Number of search results to fetch[/]",
        default=config.DEFAULT_SEARCH_LIMIT
    )
    # Clamp limit
    limit = max(1, min(limit, config.MAX_SEARCH_LIMIT))

    search_results = []
    deep_contents = None

    # Step 1: Web Search
    with console.status("[bold green]Querying search engine...[/]") as status:
        try:
            search_results = search_client.search(query, num_results=limit)
        except Exception as e:
            console.print(f"\n[bold red]Search Error:[/] {e}")
            input("\nPress Enter to return to main menu...")
            return

    if not search_results:
        console.print("\n[bold red]No search results found for this query.[/]")
        input("\nPress Enter to return to main menu...")
        return

    # Step 2: Content Scrape (Deep Mode only)
    if mode == "deep":
        urls = [r["url"] for r in search_results]
        with console.status("[bold green]Downloading and parsing web pages in parallel...[/]") as status:
            try:
                deep_contents = scraper.scrape_urls_parallel(urls)
            except Exception as e:
                console.print(f"\n[bold red]Scraping Error:[/] {e}")
                # Fallback to snippets by keeping deep_contents as None
                deep_contents = None

    # Step 3: LLM Synthesis
    llm = OpenAIClient()
    answer = ""
    with console.status("[bold green]Synthesizing answer with OpenAI LLM...[/]") as status:
        answer, _ = llm.synthesize_answer(query, search_results, deep_contents)

    # Render results
    print_welcome_banner()
    console.print(Panel(f"[bold white]Query:[/] [cyan]{query}[/]\n[bold white]Mode:[/] [green]{mode.upper()}[/]", border_style="cyan"))
    
    console.print("\n[bold yellow]🤖 AI Synthesized Answer[/]\n")
    console.print(Markdown(answer))
    console.print("\n" + "="*60 + "\n")
    
    # Render sources table
    sources_table = Table(title="[bold yellow]Sources Used for This Answer[/]", border_style="dim blue")
    sources_table.add_column("Ref", justify="center", style="bold cyan")
    sources_table.add_column("Title", style="white")
    sources_table.add_column("Source URL / Domain", style="dim green")
    
    for i, res in enumerate(search_results, 1):
        # Clean URL domain for easier reading
        url = res["url"]
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        sources_table.add_row(f"[{i}]", res["title"], f"[link={url}]{domain}[/link]")
        
    console.print(sources_table)

    # Save to history automatically
    utils.save_to_history(query, mode, answer, search_results)

    # Action menu loop for this search
    while True:
        console.print("\n[bold]Options:[/] [1] Ask Follow-up (Chat)  [2] Export Report  [3] New Search  [4] Main Menu")
        choice = Prompt.ask("[bold yellow]What would you like to do?[/]", choices=["1", "2", "3", "4"])

        if choice == "1":
            run_chat_session(llm, query, search_results, deep_contents)
            break
        elif choice == "2":
            try:
                file_path = utils.export_report(query, mode, answer, search_results)
                console.print(f"\n[bold green]Success![/] Report exported to: [cyan]{file_path}[/]")
            except Exception as e:
                console.print(f"\n[bold red]Export Failed:[/] {e}")
        elif choice == "3":
            run_ai_search(search_client, scraper)
            break
        elif choice == "4":
            break

def run_chat_session(llm: OpenAIClient, query: str, search_results: list[dict], deep_contents: list[str]):
    """Handles an interactive chat session about the retrieved search results."""
    clear_terminal()
    console.print(
        Panel(
            Align.center(f"[bold cyan]💬 AI SEARCH CHAT SESSION\n[white]Query: {query}"),
            border_style="bold green"
        )
    )
    console.print("[dim]You can now ask follow-up questions about the search results. Type 'exit' to return to menu.[/]\n")

    # Start the chat session
    with console.status("[bold green]Starting chat session with search context...[/]"):
        try:
            chat, first_answer = llm.start_chat_session(query, search_results, deep_contents)
        except Exception as e:
            console.print(f"[bold red]Chat Initialization Error:[/] {e}")
            input("\nPress Enter to return...")
            return

    console.print("[bold cyan]AI Assistant:[/] Based on your search...")
    console.print(Markdown(first_answer))
    console.print("-" * 50)

    # Chat loop
    while True:
        try:
            follow_up = Prompt.ask("\n[bold yellow]You[/]")
            if follow_up.lower().strip() in ["exit", "quit"]:
                break
                
            if not follow_up.strip():
                continue

            with console.status("[bold green]Thinking...[/]"):
                response = chat.send_message(follow_up)
            
            console.print(f"\n[bold cyan]AI Assistant:[/]")
            console.print(Markdown(response.text))
            console.print("-" * 50)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/] {e}")

def view_history():
    """Displays the query history table and allows viewing specific answers."""
    while True:
        print_welcome_banner()
        history = utils.load_history()
        
        if not history:
            console.print("\n[bold yellow]No search history found.[/]")
            input("\nPress Enter to return to main menu...")
            break
            
        history_table = Table(title="[bold yellow]Search History (Latest First)[/]", border_style="blue")
        history_table.add_column("No.", justify="center", style="bold cyan")
        history_table.add_column("Time", style="dim white")
        history_table.add_column("Mode", style="green")
        history_table.add_column("Query", style="white")
        
        for idx, record in enumerate(history, 1):
            # Parse timestamp for cleaner print
            try:
                dt = datetime.fromisoformat(record["timestamp"])
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                time_str = record["timestamp"]
            
            history_table.add_row(f"{idx}", time_str, record.get("mode", "fast").upper(), record["query"])
            
        console.print(history_table)
        console.print("\n[bold]Options:[/] [Index #] View Detail  [c] Clear All  [m] Main Menu")
        action = Prompt.ask("[bold yellow]Choose action[/]")
        
        if action.lower() == "m":
            break
        elif action.lower() == "c":
            if Confirm.ask("[red]Are you sure you want to clear ALL history?[/]"):
                utils.clear_history()
                console.print("[green]History cleared successfully![/]")
                input("\nPress Enter to continue...")
        else:
            try:
                idx = int(action)
                if 1 <= idx <= len(history):
                    record = history[idx - 1]
                    print_welcome_banner()
                    console.print(Panel(f"[bold white]Query:[/] [cyan]{record['query']}[/]\n[bold white]Time:[/] [dim]{record['timestamp']}[/]\n[bold white]Mode:[/] [green]{record.get('mode', 'fast').upper()}[/]", border_style="cyan"))
                    
                    console.print("\n[bold yellow]🤖 AI Synthesized Answer[/]\n")
                    console.print(Markdown(record["answer"]))
                    console.print("\n" + "="*60 + "\n")
                    
                    # Render sources list
                    console.print("[bold yellow]Sources Citations Used:[/]")
                    for i, source in enumerate(record.get("sources", []), 1):
                        console.print(f"[{i}] {source.get('title')} - [dim green]{source.get('url')}[/]")
                        
                    input("\nPress Enter to return to history list...")
                else:
                    console.print("[red]Invalid index number.[/]")
                    input("\nPress Enter to continue...")
            except ValueError:
                console.print("[red]Invalid input. Please enter a number, 'c', or 'm'.[/]")
                input("\nPress Enter to continue...")

def edit_settings():
    """Allows updating settings like the LLM model choice and checking key status."""
    while True:
        print_welcome_banner()
        
        # Display current status
        status_table = Table(title="[bold yellow]System Settings & Status[/]", border_style="cyan")
        status_table.add_column("Configuration Key", style="bold white")
        status_table.add_column("Current Status / Value", style="green")
        
        # API Keys validation
        openai_status = "[bold green]Configured ✅[/]" if config.has_openai_key() else "[bold red]Missing ❌ (AI synthesis disabled)[/]"
        
        status_table.add_row("OPENAI_API_KEY", openai_status)
        status_table.add_row("Default LLM Model", config.DEFAULT_MODEL)
        status_table.add_row("Max Search Count", str(config.DEFAULT_SEARCH_LIMIT))
        status_table.add_row("Content Scrape Limit", f"{config.MAX_CHARS_PER_PAGE} chars")
        status_table.add_row("History File Path", config.HISTORY_FILE)
        
        console.print(status_table)
        
        console.print("\n[bold]Options:[/] [1] Change LLM Model  [2] Adjust Default Search Limit  [m] Main Menu")
        choice = Prompt.ask("[bold yellow]Choose action[/]", choices=["1", "2", "m"])
        
        if choice == "m":
            break
        elif choice == "1":
            console.print("\nAvailable models:")
            for i, model in enumerate(config.SUPPORTED_MODELS, 1):
                console.print(f"  [{i}] {model}")
            idx = IntPrompt.ask("Select model index", default=1)
            if 1 <= idx <= len(config.SUPPORTED_MODELS):
                config.DEFAULT_MODEL = config.SUPPORTED_MODELS[idx - 1]
                console.print(f"[green]Default model updated to {config.DEFAULT_MODEL}[/]")
            else:
                console.print("[red]Invalid index.[/]")
            input("\nPress Enter to continue...")
        elif choice == "2":
            limit = IntPrompt.ask(f"Enter search limit (1-{config.MAX_SEARCH_LIMIT})", default=config.DEFAULT_SEARCH_LIMIT)
            if 1 <= limit <= config.MAX_SEARCH_LIMIT:
                config.DEFAULT_SEARCH_LIMIT = limit
                console.print(f"[green]Default search limit updated to {config.DEFAULT_SEARCH_LIMIT}[/]")
            else:
                console.print("[red]Limit must be between 1 and 10.[/]")
            input("\nPress Enter to continue...")

def main():
    """Main interactive terminal loop."""
    # Ensure environment variables are loaded
    config.print_setup_warning()
    
    # Initialize components
    search_client = SearchClient()
    scraper = WebScraper()
    
    while True:
        print_welcome_banner()
        console.print("\n[bold yellow]=== MAIN MENU ===[/]")
        console.print("  [1] 🔎 AI Search (Fast / Deep)")
        console.print("  [2] 📜 View Search History")
        console.print("  [3] ⚙️ Settings & API Status")
        console.print("  [4] ❌ Exit")
        
        choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4"], default="1")
        
        if choice == "1":
            run_ai_search(search_client, scraper)
        elif choice == "2":
            view_history()
        elif choice == "3":
            edit_settings()
        elif choice == "4":
            print_welcome_banner()
            console.print("\n[bold green]Thank you for using AI Custom Search Engine! Goodbye! 👋[/]\n")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold green]Program terminated by user. Goodbye! 👋[/]\n")
        sys.exit(0)
