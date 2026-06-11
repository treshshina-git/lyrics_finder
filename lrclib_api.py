import aiohttp


async def get_lyrics(artist, title):

    async with aiohttp.ClientSession() as session:

        # Поиск по названию
        search_url = "https://lrclib.net/api/search"

        async with session.get(
            search_url,
            params={
                "track_name": title
            }
        ) as response:

            if response.status != 200:
                return None

            songs = await response.json()

        if not songs:
            return None

        # Ищем максимально похожего исполнителя
        for song in songs:

            song_artist = (
                song.get("artistName", "")
                .lower()
            )

            if artist.lower() in song_artist:

                return (
                    song.get("plainLyrics")
                    or song.get("syncedLyrics")
                )

        # Берём первый результат
        return (
            songs[0].get("plainLyrics")
            or songs[0].get("syncedLyrics")
        )
