# Weather Telegram Bot

A Telegram bot that fetches current weather data by city name using the Open-Meteo API.

## Stack

- Python
- Aiogram
- FastAPI
- aiohttp
- Open-Meteo API

## Features

- Sends weather data based on the city name
- Supports city names in both Russian and English
- Reply Keyboard
- FSM

## Project structure

```
bot.py                 # Telegram bot
api.py                 # FastAPI application
services/weather.py    # Weather service
```

## Installation

```bash
git clone https://github.com/Griz-Wold/weather-telegram-bot
cd weather-telegram-bot

Create .env file:
BOT_TOKEN=your_telegram_bot_token

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Run API

```bash
uvicorn api:app --reload
```

## Run Bot

```bash
python bot.py
```
