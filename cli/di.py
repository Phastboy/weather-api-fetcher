from features.clients.adapters.pirate_weather_client import PirateWeatherClient
from features.clients.ports.weather_client import WeatherClient

_weather_client_instance = None


def get_weather_client() -> WeatherClient:
    """Lazy loads the weather client to prevent import-time crashes."""
    global _weather_client_instance
    if _weather_client_instance is None:
        _weather_client_instance = PirateWeatherClient()
    return _weather_client_instance
