import typer
from cli import di
from cli import views

app = typer.Typer(help="A beautiful CLI to fetch real-time weather data.")


@app.command()
def fetch(city: str):
    """Fetches the current weather for a specific city."""
    try:
        client = di.get_weather_client()
        report = client.fetch_weather(city)

        views.display_weather(report)
    except ValueError as e:
        views.display_error(str(e))


@app.command()
def version():
    """Prints the current version of the application."""
    views.console.print("Weather API Fetcher v0.1.0")
