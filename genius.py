import lyricsgenius
import os

genius = lyricsgenius.Genius(
    os.getenv("GENIUS_TOKEN")
)


def search_song(query):

    song = genius.search_song(query)

    if not song:
        return None

    return {
        "title": song.title,
        "artist": song.artist,
        "lyrics": song.lyrics
    }
