from dataclasses import dataclass


@dataclass
class WeatherReport:
    city: str
    temperature: float
    description: str
    humidity: int

    @property
    def formatted_temperature(self) -> str:
        """Returns the temperature nicely formatted with the Celsius symbol."""
        return f"{self.temperature:.1f}°C"

    @property
    def formatted_humidity(self) -> str:
        """Returns the humidity formatted as a percentage."""
        return f"{self.humidity}%"

    def __str__(self) -> str:
        return f"{self.city}: {self.description.title()}, {self.formatted_temperature}, Humidity: {self.formatted_humidity}"
