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

            if response.status != 200:
                print(
                    f"Genius API error: {response.status}"
                )
                return []

            data = await response.json()

            hits = data["response"]["hits"]

            if not hits:
                return []

            results = []

            for hit in hits[:45]:

                song = hit["result"]

                results.append({
                    "title": song["title"],
                    "artist": song["primary_artist"]["name"],
                    "url": song["url"],
                    "id": song["id"]
                })

            print(
                f"Found {len(results)} songs"
            )

            return results
