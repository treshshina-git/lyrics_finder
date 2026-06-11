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

        for page in range(1, 6):
            async with session.get(
                url,
                headers=headers,
                params={
                    "q": query,
                    "page": page
                }
            ) as response:
                data = await response.json()
                hits = data["response"]["hits"]
                if not hits:
                    break
                    for hit in hits:
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
            print("HITS:", len(hits))
            print("RESULTS:", len(results))

            return results
