import aiohttp
from typing import TypedDict

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=5)

CURRENT_FIELDS = "temperature_2m,apparent_temperature,wind_speed_10m"


class Coordinates(TypedDict):
    name: str
    lat: float
    lon: float


class Weather(TypedDict):
    temperature: int
    apparent_temperature: int
    wind_speed: int


async def _fetch_json(
    session: aiohttp.ClientSession, url: str, params: dict[str, object]
) -> dict:
    """Извлекает данные в JSON из внешнего API"""

    async with session.get(
        url, params=params, timeout=REQUEST_TIMEOUT, raise_for_status=True
    ) as response:
        return await response.json()


async def get_coordinates(
    session: aiohttp.ClientSession, city: str
) -> Coordinates | None:
    """Возвращает координаты первого города или None"""

    city = city.strip()
    if not city:
        return None

    params = {"name": city, "count": 1, "format": "json", "language": "ru"}
    data = await _fetch_json(session, GEOCODING_URL, params)

    if "results" not in data or not data["results"]:
        return None

    result = data["results"][0]

    if not all(k in result for k in ("name", "latitude", "longitude")):
        return None

    coordinates: Coordinates = {
        "name": result["name"],
        "lat": result["latitude"],
        "lon": result["longitude"],
    }

    return coordinates


async def get_weather(
    session: aiohttp.ClientSession, lat: float, lon: float
) -> Weather | None:
    """Возвращает текущую погоду по координатам или None"""

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": CURRENT_FIELDS,
        "timezone": "auto",
        "wind_speed_unit": "ms",
    }
    data = await _fetch_json(session, WEATHER_URL, params)

    if "current" not in data or not data["current"]:
        return None

    result = data["current"]

    if not all(
        k in result
        for k in ("temperature_2m", "apparent_temperature", "wind_speed_10m")
    ):
        return None

    weather: Weather = {
        "temperature": round(result["temperature_2m"]),
        "apparent_temperature": round(result["apparent_temperature"]),
        "wind_speed": round(result["wind_speed_10m"]),
    }

    return weather
