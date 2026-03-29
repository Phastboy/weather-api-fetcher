# features/clients/adapters/pirate_weather_client.py
import os
import requests
from dotenv import load_dotenv
from features.models.weather import WeatherReport
from features.clients.ports.weather_client import WeatherClient

load_dotenv()


def get_coordinates(city: str) -> tuple[str, str, str]:
    """Converts a city name into latitude and longitude using OpenStreetMap."""
    headers = {"User-Agent": "WeatherAppCLI/1.0"}
    base_url = "https://nominatim.openstreetmap.org/search"

    params = {"q": city, "limit": 1, "format": "json"}

    try:
        response = requests.get(base_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError(
                f"Could not find coordinates for '{city}'. Check the spelling!"
            )

        first_result = data[0]

        lat = first_result.get("lat")
        lon = first_result.get("lon")
        name = first_result.get("name")

        if not lat or not lon or not name:
            raise ValueError(
                f"Incomplete coordinate data returned by geocoder for '{city}'."
            )

        return lat, lon, name

    except requests.exceptions.RequestException:
        raise ValueError("Network error: Could not connect to the geocoding service.")


class PirateWeatherClient(WeatherClient):
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "CRITICAL: OPENWEATHER_API_KEY is missing from your .env file."
            )

    def fetch_weather(self, city: str) -> WeatherReport:
        """Fetches live data from Pirate Weather."""

        lat, lon, resolved_city_name = get_coordinates(city)

        url = f"https://api.pirateweather.net/forecast/{self.api_key}/{lat},{lon}"
        params = {"units": "si"}

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code in (401, 403):
                raise ValueError(
                    "Invalid API Key. Make sure your Pirate Weather key is in your .env file."
                )

            response.raise_for_status()
            data = response.json()

            currently = data.get("currently", {})

            return WeatherReport(
                city=resolved_city_name.split(",")[0],
                temperature=currently.get("temperature", 0.0),
                description=currently.get("summary", "Unknown"),
                humidity=int(currently.get("humidity", 0) * 100),
            )

        except requests.exceptions.RequestException:
            raise ValueError("Network error: Could not connect to Pirate Weather.")
