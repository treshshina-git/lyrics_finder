import aiohttp
import os

GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")


async def search_song(query: str):
    url = "https://api.genius.com/search"

    headers = {
        "Authorization": f"Bearer {GENIUS_TOKEN}"
    }

    params = {
        "q": query
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
            params=params
        ) as response:

            if response.status != 200:
                return None

            data = await response.json()

            hits = data["response"]["hits"]

            if not hits:
                return None

            song = hits[0]["result"]

            return {
                "title": song["title"],
                "artist": song["primary_artist"]["name"],
                "url": song["url"]
            }