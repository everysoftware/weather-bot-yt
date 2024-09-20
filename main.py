import asyncio
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, F, types
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")
api_key = os.getenv("API_KEY")

bot = Bot(token)
dp = Dispatcher()


@dp.message(F.location)
async def send_forecast(message: types.Message) -> None:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lon": message.location.longitude,
        "lat": message.location.latitude,
        "appid": api_key,
        "units": "metric"
    }
    async with aiohttp.ClientSession() as client:
        async with client.get(base_url, params=params) as response:
            weather = await response.json()
            main = weather["main"]

            await message.answer(f"The weather: {main["temp"]} °C (feels like: {main["feels_like"]} °C) ☁️")


logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
