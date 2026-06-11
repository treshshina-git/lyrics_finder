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

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "🎵 Отправьте название песни или строку из песни."
    )

@dp.message()
async def find_song(message: Message):

    query = message.text.strip()

    if len(query) > 200:
        await message.answer(
            "Слишком длинный запрос."
        )
        return

    status = await message.answer(
        "🔍 Ищу песню..."
    )

    song = await search_song(query)
    print(song)
    if not song:
        await status.edit_text(
            "❌ Песня не найдена."
        )
        return

    lyrics = await get_lyrics(
        song["artist"],
        song["title"]
    )
    
    if not lyrics:
        await message.answer(
           f"🎵 {artist} - {title}\n\n"
           f"Текст не найден в LRCLIB.\n"
           f"Открыть Genius:\n{url}"
        )
        return
        await status.edit_text(
            f"✅ Найдено:\n"
            f"{song['artist']} - {song['title']}"
        )
        
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
