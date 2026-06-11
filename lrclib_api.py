import aiohttp


async def get_lyrics(artist, title):

    url = "https://lrclib.net/api/search"

    params = {
        "artist_name": artist,
        "track_name": title
    }

    async with aiohttp.ClientSession() as session:

        async with session.get(
            url,
            params=params
        ) as response:

            if response.status != 200:
                return None

            data = await response.json()

            if not data:
                return None

            song = data[0]

            lyrics = (
                song.get("plainLyrics")
                or song.get("syncedLyrics")
            )

            return lyrics