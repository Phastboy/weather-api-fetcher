from rich.console import Console
from rich.panel import Panel
from features.models.weather import WeatherReport

console = Console()


def display_weather(report: WeatherReport) -> None:
    """Renders a beautiful weather card."""
    content = (
        f"[bold cyan]Temperature:[/bold cyan] {report.formatted_temperature}\n"
        f"[bold cyan]Condition:[/bold cyan]   {report.description.title()}\n"
        f"[bold cyan]Humidity:[/bold cyan]    {report.formatted_humidity}"
    )

    panel = Panel(
        content,
        title=f"🌤️  Weather Report: [bold yellow]{report.city}[/bold yellow]",
        expand=False,
        border_style="blue",
    )
    console.print(panel)


def display_error(message: str) -> None:
    console.print(f"[bold red]✘ Error:[/bold red] {message}")
