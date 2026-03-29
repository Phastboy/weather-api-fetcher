# Weather API Fetcher 🌤️

A robust, beautifully formatted Command Line Interface (CLI) for fetching real-time weather data.

Built using modern Python tooling (`uv`, `Typer`, `Rich`) and strictly adhering to **Clean Architecture** (Ports and Adapters), this tool decouples the core application from external network dependencies.

### 📝 Note to Reviewers on API Selection
During development, the OpenWeatherMap API experienced 500 Internal Server Error outage. To ensure continuous operation and meet project deadlines, the data provider was dynamically swapped out.

The application utilizes **OpenStreetMap (Nominatim)** for geocoding and the **Pirate Weather API** for meteorological data. Because the application was built using pure Dependency Injection, this pivot required zero changes to the UI or core business logic, only a new adapter was written.

## ✨ Key Features
* **Elegant UI:** Utilizes `Rich` to render floating, high-contrast weather panels instead of raw JSON.
* **Robust Error Handling:** Comprehensively catches and handles network timeouts, invalid API keys, 404 Not Found errors, and missing JSON keys with user-friendly terminal messages.
* **Safe Geocoding:** Automatically sanitizes and URL-encodes city names (handling spaces and special characters safely).
* **Lazy Loading:** Instantiates API clients only when requested, ensuring the CLI (`--help`, `version`) remains lightning-fast and functional even if environment variables are missing.

## 🚀 Prerequisites & Installation

This project utilizes [uv](https://github.com/astral-sh/uv) for lightning-fast dependency and environment management.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Phastboy/weather-api-fetcher.git
   cd weather-api-fetcher
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory. Add your Pirate Weather API key (we retained the OpenWeather variable name for backward compatibility):
   ```env
   OPENWEATHER_API_KEY=your_pirate_weather_api_key_here
   ```
   *(Note: The `.env` file is strictly ignored in `.gitignore` to prevent credential leaks).*

3. **Install Dependencies (if not using `uv run` directly):**
   ```bash
   uv sync
   ```

## 💻 Usage

`uv` handles the virtual environment natively. Simply run the following commands:

**View the Help Menu:**
```bash
uv run python main.py --help
```

**Fetch Weather for a City:**
```bash
uv run python main.py fetch lagos
uv run python main.py fetch "new york"
```

**Check Application Version:**
```bash
uv run python main.py version
```

## 🏗️ Architecture
* `features/models/`: The pure `WeatherReport` dataclass.
* `features/clients/ports/`: The abstract `WeatherClient` interface.
* `features/clients/adapters/`: Concrete implementations (e.g., `PirateWeatherClient`).
* `cli/`: The Typer and Rich presentation layer.
