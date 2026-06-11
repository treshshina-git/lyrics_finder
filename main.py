from aiogram import Bot
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from dotenv import load_dotenv

import asyncio
import os

from genius import search_song

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Отправь фрагмент текста песни 🎵"
    )


@dp.message()
async def lyrics_search(message: Message):

    query = message.text

    await message.answer(
        "🔎 Ищу..."
    )

    result = await search_song(query)

    if not result:
        await message.answer(
            "Ничего не найдено"
        )
        return

    text = (
        f"🎵 {result['artist']} - {result['title']}\n\n"
        f"{result['url']}"
    )

    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())