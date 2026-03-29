import os
import requests
from dotenv import load_dotenv
from features.models.weather import WeatherReport
from features.clients.ports.weather_client import WeatherClient

load_dotenv()


def get_coordinates(city: str) -> tuple[str, str, str]:
    """Converts a city name into latitude and longitude using OpenStreetMap."""
    # Nominatim requires a User-Agent
    headers = {"User-Agent": "WeatherAppCLI/1.0"}
    url = f"https://nominatim.openstreetmap.org/search?q={city}&limit=1&format=json"

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError(
            f"Could not find coordinates for '{city}'. Check the spelling!"
        )

    return data[0]["lat"], data[0]["lon"], data[0]["name"]


class PirateWeatherClient(WeatherClient):
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("CRITICAL: API_KEY is missing from your .env file.")

    def fetch_weather(self, city: str) -> WeatherReport:
        """Fetches live data from Pirate Weather."""

        # 1.  convert the city name to coordinates
        lat, lon, resolved_city_name = get_coordinates(city)

        # 2. Construct the Pirate Weather URL
        url = f"https://api.pirateweather.net/forecast/{self.api_key}/{lat},{lon}"

        # Pirate Weather uses 'si' for Celsius.
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

            # 3. Parse Pirate Weather's unique JSON structure
            return WeatherReport(
                # Use the clean name from the map (e.g., "Lagos, Nigeria" instead of just "lagos")
                city=resolved_city_name.split(",")[0],
                temperature=currently.get("temperature", 0.0),
                description=currently.get("summary", "Unknown"),
                # Pirate Weather returns humidity as a decimal (e.g., 0.75). We multiply by 100 for your UI.
                humidity=int(currently.get("humidity", 0) * 100),
            )

        except requests.exceptions.RequestException:
            raise ValueError("Network error: Could not connect to Pirate Weather.")
