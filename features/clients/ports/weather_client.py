from abc import ABC, abstractmethod
from features.models.weather import WeatherReport


class WeatherClient(ABC):
    """
    The abstract contract for fetching weather data.
    Any class that inherits from this MUST implement the fetch_weather method.
    """

    @abstractmethod
    def fetch_weather(self, city: str) -> WeatherReport:
        """
        Fetches the current weather for a given city.

        Args:
            city: The name of the city to search for.

        Returns:
            WeatherReport: A perfectly structured domain model.

        Raises:
            ValueError: If the city is not found or the network request fails.
        """
        pass
