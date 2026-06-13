# Weather Telegram Bot

Телеграм-бот для получения текущей погоды по названию города. После получения названия через Open-Meteo API извлекает данные и отправляет их пользователю.

## Stack

- Python
- Aiogram
- FastAPI
- aiohttp
- Open-Meteo API

## Features

- Отправляет данные о погоде по названию города
- Поддерживает названия городов на русском и английском языках
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

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Run API

```bash
uvicorn api:app --reload
```

# Run Bot

```bash
python bot.py
```
