from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
URL = "http://127.0.0.1:8000/weather"


class WeatherState(StatesGroup):
    waiting_for_city = State()


weather_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Узнать погоду")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)


async def weather_answer(city: str) -> str:
    params = {"city": city}
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params) as response:
            if response.status != 200:
                return "Не удалось получить погоду"

            data = await response.json()
    return (
        f"Город: {data['name']}\n"
        f"🌡Температура: {data['temperature']}°C\n"
        f"🤔Ощущается как: {data['apparent_temperature']}°C\n"
        f"💨Скорость ветра: {data['wind_speed']} м/с"
    )


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.text == "Узнать погоду")
async def weather_button_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Укажите название города")
    await state.set_state(WeatherState.waiting_for_city)


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "Привет! Я бот, который дает прогноз погоды.\n"
        "Чтобы узнать погоду используйте кнопку Узнать погоду или команду /weather\n"
        "Для подробностей используйте команду /help",
        reply_markup=weather_keyboard,
    )


@dp.message(WeatherState.waiting_for_city)
async def city_from_button_handler(message: Message, state: FSMContext) -> None:
    city = message.text.strip()
    await state.clear()
    await message.answer(await weather_answer(city))


@dp.message(Command("weather"))
async def city_handler(message: Message) -> None:
    request = message.text.split(maxsplit=1)
    if len(request) <= 1:
        await message.answer("Вы не указали город")
        return

    city = request[1]
    await message.answer(await weather_answer(city))


@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Как пользоваться:\n"
        "1. Нажмите кнопку Узнать погоду и укажите город;\n"
        "2. Или напишите команду /weather и укажите город"
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
