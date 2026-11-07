import logging
import os

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from fashion_store_rag.agent.orchestrator import run_agent

console = Console()


def configure_logging() -> None:
    """Enable logging when LOG_LEVEL is set (e.g. LOG_LEVEL=INFO); off by default."""
    level = os.getenv("LOG_LEVEL")

    if not level:
        return

    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def display_welcome():
    welcome = Text()
    welcome.append("FASHION STORE AI\n", style="bold cyan")
    welcome.append("Your personal shopping assistant - ", style="white")
    welcome.append("Type /help for commands or /exit to quit", style="dim italic")

    console.print(
        Panel(
            welcome,
            border_style="cyan",
            padding=(1, 3),
        )
    )


def display_help():
    console.print(
        Panel(
            "[bold cyan]/help[/bold cyan]     Show available commands\n"
            "[bold cyan]/clear[/bold cyan]    Clear the terminal\n"
            "[bold cyan]/exit[/bold cyan]     Exit the application",
            title="Available Commands",
            border_style="cyan",
        )
    )


def display_response(answer: str):
    console.print(
        Panel(
            Markdown(answer),
            title="[bold green]Fashion Store Assistant[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )


def main():
    configure_logging()
    display_welcome()

    while True:
        try:
            query = console.input("[bold white]You[/bold white] : ").strip()

            if not query:
                continue

            if query.lower() in ("/exit", "/quit"):
                console.print(
                    "\n[bold cyan]Thanks for visiting Fashion Store![/bold cyan]"
                )
                break

            if query.lower() == "/help":
                display_help()
                continue

            if query.lower() == "/clear":
                console.clear()
                display_welcome()
                continue

            # Run the existing agent, surfacing its current stage live.
            with console.status(
                "[bold yellow]Thinking...[/bold yellow]",
                spinner="dots",
            ) as status:
                result = run_agent(
                    query,
                    on_status=lambda message: status.update(
                        f"[bold yellow]{message}...[/bold yellow]"
                    ),
                )

            answer = result.get("answer")

            if answer:
                console.print("[bold cyan]AI[/bold cyan] : ", answer)
                console.print()
            else:
                console.print(
                    "[yellow]The assistant couldn't generate a response.[/yellow]"
                )

        except KeyboardInterrupt:
            console.print("\nExiting.")
            break

        except EOFError:
            console.print("\nExiting.")
            break

        except Exception as error:  # noqa: BLE001
            console.print(f"\n[red]Something went wrong:[/red] {error}\n")


if __name__ == "__main__":
    main()
