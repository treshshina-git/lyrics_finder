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

search_cache = {}

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

    await message.answer(
        "🔍 Ищу песню..."
    )

    songs = await search_song(query)
    print(songs)
    print(len(songs))
    if not songs:
        await message.answer(
            "❌ Ничего не найдено"
        )
        return

    search_cache[message.from_user.id] = songs


    def build_page(songs, page=0, per_page=5):
        builder = InlineKeyboardBuilder()
        start = page * per_page
        end = start + per_page
        page_songs = songs[start:end]
        for index, song in enumerate(page_songs, start=start):
            builder.button(
                text=f"{song['artist']} - {song['title'][:25]}",
                callback_data=f"song_{index}"
            )
            nav = []
            if page > 0:
                nav.append({
                    "text": "⬅️",
                    "data": f"page_{page-1}"
                })
                nav.append({
                    "text": f"{page+1}/{(len(songs)-1)//per_page+1}",
                    "data": "noop"
                })
                if end < len(songs):
                    nav.append({
                        "text": "➡️",
                        "data": f"page_{page+1}"
                    })
                    for item in nav:
                        builder.button(
                            text=item["text"],
                            callback_data=item["data"]
                        )
                    builder.adjust(1)
                if len(nav):
                    builder.adjust(
                        *([1] * len(page_songs)),
                        len(nav)
                    )
            return builder
            builder = build_page(
                songs,
                page=0
            )
    builder.adjust(1)

    await message.answer(
        "🎵 Выберите песню:",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data.startswith("song_"))
async def select_song(callback: CallbackQuery):

    index = int(
        callback.data.replace(
            "song_",
            ""
        )
    )

    songs = search_cache.get(
        callback.from_user.id
    )

    if not songs:
        await callback.answer(
            "Поиск устарел",
            show_alert=True
        )
        return

    song = songs[index]

    artist = song["artist"]
    title = song["title"]
    url = song["url"]

    await callback.answer()

    await callback.message.answer(
        f"🔍 Получаю текст:\n"
        f"{artist} - {title}"
    )

    lyrics = await get_lyrics(
        artist,
        title
    )

    if not lyrics:
        await callback.message.answer(
            f"🎵 {artist} - {title}\n\n"
            f"Текст не найден в LRCLIB.\n\n"
            f"🔗 {url}"
        )
        return

    await callback.message.answer(
        f"🎵 {artist} - {title}"
    )

    for part in split_text(lyrics):
        await callback.message.answer(part)
    

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
