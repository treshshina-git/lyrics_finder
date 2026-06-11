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
    await message.answer(
        "🎵 Выберите песню:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("page_"))
async def page_change(callback: CallbackQuery):

    page = int(
        callback.data.replace(
            "page_",
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

    builder = build_page(
        songs,
        page=page
    )

    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )

    await callback.answer()
@dp.callback_query(F.data == "noop")
async def noop(callback: CallbackQuery):
    await callback.answer()

@dp.callback_query(F.data.startswith("page_"))
async def page_change(callback: CallbackQuery):

    page = int(
        callback.data.replace(
            "page_",
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

    builder = build_page(
        songs,
        page=page
    )

    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )

    await callback.answer()
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
