from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

raw_songs = {
    0: {
        "artist":"Daft Punk",
        "name":"Instant Crush",
        "platform": "YouTube",
        "link":"https://music.youtube.com/watch?v=khnokW3Mw24"
    },
    1: {
        "artist":"Pink Floyd",
        "name":"Wish you were here",
        "platform": "YouTube",
        "link":"https://music.youtube.com/watch?v=hjpF8ukSrvk"
    },
    2: {
        "artist":"Alim Qasimov & Michel Godard",
        "name":"Trace of Grace",
        "platform": "YouTube",
        "link":"https://music.youtube.com/watch?v=KUn9ltbYbC0&feature=share"
    },
    3: {
        "artist":"ABBA",
        "name":"Gimme! Gimme! Gimme! (A Man After Midnight)",
        "link":"https://music.youtube.com/watch?v=XEjLoHdbVeE",
        "platform": "Spotify",
        "shared_by": "JAXA",
    }
}


class Platform(str, Enum):
    spotify = "Spotify"
    youtube = "YouTube"
    youtube_music = "YouTube Music"
    other = "Other"

# TODO Find the way of generating id 

class Song(BaseModel):
    name: str
    artist: str
    link: str
    platform: Platform
    shared_by: str | None = None


DB = {id: Song(**song_data) for id, song_data in raw_songs.items()}

# TODO Have better structured API endpoints

@app.post("/v1/songs/")
async def add_song(song: Song) -> Song:
    new_id = max(DB.keys()) + 1
    # TODO Integrate proper database logic (SQLAlchemy, SQLite ??)
    # https://fastapi.tiangolo.com/tutorial/sql-databases/
    DB[new_id] = song
    return song

@app.get("/v1/songs/{song_id}")
async def get_song(song_id: int) -> Song:
    return DB[song_id]

@app.get("/v1/songs/")
async def get_songs() -> dict[int, Song]:
    return DB
