import typer
from cli import di
from cli import views

app = typer.Typer(help="A beautiful CLI to fetch real-time weather data.")


@app.command()
def fetch(city: str):
    """Fetches the current weather for a specific city."""
    try:
        # 1. Ask the injected client for the data
        report = di.weather_client.fetch_weather(city)

        # 2. Hand the pure domain model to the view
        views.display_weather(report)
    except ValueError as e:
        # Catches exception
        views.display_error(str(e))


@app.command()
def version():
    """Prints the current version of the application."""
    views.console.print("Weather API Fetcher v0.1.0")
