import time
from features.models.weather import WeatherReport
from features.clients.ports.weather_client import WeatherClient


class MockWeatherClient(WeatherClient):
    """
    A temporary mock adapter that returns hardcoded weather data.
    Used for testing the UI while the real API is down or being developed.
    """

    def __init__(self):
        #  "fake" database of weather responses
        self.mock_data = {
            "lagos": {"temp": 32.5, "desc": "scattered clouds", "humidity": 75},
            "london": {"temp": 12.0, "desc": "light rain", "humidity": 82},
            "tokyo": {"temp": 18.2, "desc": "clear sky", "humidity": 60},
            "new york": {"temp": 22.1, "desc": "overcast clouds", "humidity": 65},
        }

    def fetch_weather(self, city: str) -> WeatherReport:
        """Simulates fetching weather data, complete with a fake network delay."""
        # 1. Simulate a slight network delay so the CLI feels real
        time.sleep(0.8)

        # 2. Normalize the input so "LAGOS" and "lagos" both work
        search_city = city.lower().strip()

        # 3. Check if we have fake data for this city
        if search_city not in self.mock_data:
            # We raise a ValueError here to simulate an API 404 Not Found error
            raise ValueError(
                f"Could not find weather data for '{city}'. Please check the spelling."
            )

        # 4. Extract the data and build the pure Domain Model
        data = self.mock_data[search_city]

        return WeatherReport(
            city=city.title(),
            temperature=data["temp"],
            description=data["desc"],
            humidity=data["humidity"],
        )
