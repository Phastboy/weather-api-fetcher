import os
import requests
from dotenv import load_dotenv
from features.models.weather import WeatherReport
from features.clients.ports.weather_client import WeatherClient

load_dotenv()


class OwmWeatherClient(WeatherClient):
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "CRITICAL: OPENWEATHER_API_KEY is missing from your .env file."
            )

        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_weather(self, city: str) -> WeatherReport:
        """Fetches live data from OpenWeatherMap."""

        params = {"q": city, "appid": self.api_key, "units": "metric"}

        try:
            # Add a 10-second timeout so the app doesn't hang forever if the internet drops
            response = requests.get(self.base_url, params=params, timeout=10)

            # Handle specific API errors
            if response.status_code == 404:
                raise ValueError(
                    f"Could not find weather data for '{city}'. Check the spelling!"
                )
            elif response.status_code == 401:
                raise ValueError(
                    "Invalid API Key. Make sure your .env file is configured correctly."
                )

            # Catch any other HTTP errors (like a 500 server crash)
            response.raise_for_status()

            data = response.json()

            return WeatherReport(
                city=data["name"],
                temperature=data["main"]["temp"],
                description=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
            )

        except requests.exceptions.RequestException:
            # This catches total internet failure or DNS issues
            raise ValueError(
                "Network error: Could not connect to OpenWeatherMap. Check your internet connection."
            )
