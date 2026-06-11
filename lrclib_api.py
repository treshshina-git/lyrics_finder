import aiohttp


async def get_lyrics(artist, title):

    async with aiohttp.ClientSession() as session:

        async with session.get(
            "https://lrclib.net/api/get",
            params={
                "artist_name": artist,
                "track_name": title
            }
        ) as response:

            if response.status != 200:
                return None

            data = await response.json()

            return (
                data.get("plainLyrics")
                or data.get("syncedLyrics")
            )
