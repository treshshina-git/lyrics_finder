from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio
import os
from genius import search_song
from lrclib_api import get_lyrics
from utils import split_text
import re
search_cache = {}
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    await message.answer("🎵 Отправьте название песни или строку из песни.")


@dp.message()
async def find_song(message: Message):

    query = message.text.strip()

    if len(query) > 200:
        await message.answer("Слишком длинный запрос.")
        return

    status = await message.answer("🔍 Ищу песню...")
    songs = await search_song(query)
    if not songs:
        await message.answer(
            "❌ Ничего не найдено"
        )
        return
        search_cache[message.from_user.id] = songs
        builder = InlineKeyboardBuilder()
        for index, song in enumerate(songs[:10]):
            builder.button(
                text=f"{index+1}. {song['title'][:40]}",
                callback_data=f"song_{index}"
            )
            builder.adjust(1)
            await message.answer(
                "🎵 Выберите песню:",
                reply_markup=builder.as_markup()
            )
            lyrics = await get_lyrics(artist, title)

    if not lyrics:
        await message.answer(f"🎵 {artist} - {title}\n\n"
                             f"Текст не найден в LRCLIB.\n"
                             f"Открыть Genius:\n{url}")
        return
        await status.edit_text(f"✅ Найдено:\n"
                               f"{song['artist']} - {song['title']}")

        def clean_title(title):
            title = re.sub(r"\(.*?\)", "", title)
            title = re.sub(r"\[.*?\]", "", title)
            return title.strip()

        def clean_artist(artist):
            artist = re.sub(r"\(.*?\)", "", artist)

        return artist.strip()

        for part in split_text(lyrics):
            await message.answer(part)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
