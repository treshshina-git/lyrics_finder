import aiohttp
import os

GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

async def search_song(query: str):

    url = "https://api.genius.com/search"

    headers = {
        "Authorization": f"Bearer {GENIUS_TOKEN}"
    }

    async with aiohttp.ClientSession() as session:

        async with session.get(
            url,
            headers=headers,
            params={"q": query}
        ) as response:

            data = await response.json()

            hits = data["response"]["hits"]

            if not hits:
                return []
                
            results = []
            for hit in hits[:10]:
                song = hit["result"]
                results.append({
                    "title": song["title"],
                    "artist": song["primary_artist"]["name"],
                    "url": song["url"]
                })
                print(results)
                return results

