import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "foggy with rime",
    51: "light drizzle",
    53: "drizzle",
    55: "heavy drizzle",
    56: "light freezing drizzle",
    57: "freezing drizzle",
    61: "light rain",
    63: "rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "freezing rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    77: "snow grains",
    80: "light rain showers",
    81: "rain showers",
    82: "heavy rain showers",
    85: "light snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with light hail",
    99: "thunderstorm with hail",
}


def get_weather_by_address(address):
    address = (address or "").strip(" ,.-")
    if not address:
        return "Please tell me the city or place whose weather you want."

    try:
        geo = requests.get(
            GEOCODING_URL,
            params={"name": address, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        geo.raise_for_status()
        results = geo.json().get("results") or []
        if not results:
            return f"I could not find a place named {address}."

        place = results[0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        weather = requests.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,apparent_temperature,weather_code,"
                    "relative_humidity_2m,wind_speed_10m"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )
        weather.raise_for_status()
        current = weather.json().get("current") or {}

        temperature = current.get("temperature_2m")
        feels_like = current.get("apparent_temperature")
        code = current.get("weather_code")
        humidity = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")

        if temperature is None:
            return "I received the weather data, but the temperature was missing."

        description = WEATHER_CODES.get(code, "current conditions")
        place_name = place.get("name", address)
        region = place.get("admin1")
        country = place.get("country")
        location = ", ".join(x for x in (place_name, region, country) if x)

        report = f"In {location}, it is {description}. The temperature is {temperature} degrees Celsius"
        if feels_like is not None:
            report += f", and it feels like {feels_like} degrees"
        if humidity is not None:
            report += f". Humidity is {humidity} percent"
        if wind is not None:
            report += f", with wind around {wind} kilometers per hour"
        return report + "."

    except requests.RequestException as e:
        print("Weather network error:", e)
        return "I could not retrieve the weather right now. Please check the internet connection."
    except (KeyError, TypeError, ValueError) as e:
        print("Weather data error:", e)
        return "I received unexpected weather data and could not read it."
