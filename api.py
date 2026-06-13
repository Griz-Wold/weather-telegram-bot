from fastapi import FastAPI, HTTPException
from services.weather import get_weather, get_coordinates
import aiohttp

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {"message": "Weather API is running"}


@app.get("/weather")
async def weather(city: str) -> dict:

    async with aiohttp.ClientSession() as session:
        coords = await get_coordinates(session, city)
        if coords is None:
            raise HTTPException(status_code=404, detail="City not found")

        result = await get_weather(session, coords["lat"], coords["lon"])
        if result is None:
            raise HTTPException(status_code=404, detail="Weather not found")

        result["name"] = coords["name"]

        return result
