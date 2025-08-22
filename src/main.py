from typing import Annotated
import secrets
import json
import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from sqlapp import crud, models, schemas

from sqlapp.database import SessionLocal, engine

BASE_URL = "http://ny_music_bank.api.javidkhasizada.xyz/"

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()

origins = json.loads(os.getenv("ORIGINS", "[]"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def data_can_be_accessed(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = str.encode(os.getenv("USERNAME", ""), encoding="utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = str.encode(os.getenv("PASSWORD", ""), encoding="utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ho Ho Hold on! It seems like your username or password didn't make it onto the 'Nice' list. Please check them twice and try entering them again, just like Santa checks his list!",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


@app.post("/v1/songs/", response_model=schemas.Song)
def create_song(
    song: schemas.SongCreate,
    _: Annotated[HTTPBasicCredentials, Depends(data_can_be_accessed)],
    db: Session = Depends(get_db),
):
    db_song = crud.get_song_by_details(
        db, artist=song.artist, name=song.name, url=song.url
    )
    if db_song:
        raise HTTPException(status_code=400, detail="Song already exists.")

    db_song = crud.create_song(db, song=song)
    links = schemas.Links(self=schemas.Link(href=f"{BASE_URL}v1/songs/{db_song.id}"))
    return schemas.Song(**db_song.to_dict(), links=links)


@app.get("/v1/songs/{song_id}", response_model=schemas.Song)
def get_song(
    song_id: int,
    _: Annotated[HTTPBasicCredentials, Depends(data_can_be_accessed)],
    db: Session = Depends(get_db),
):
    db_song = crud.get_song_by_id(db, song_id=song_id)
    links = schemas.Links(self=schemas.Link(href=f"{BASE_URL}v1/songs/{db_song.id}"))
    return schemas.Song(**db_song.to_dict(), links=links)


@app.get("/v1/songs/", response_model=list[schemas.Song])
def get_songs(
    _: Annotated[HTTPBasicCredentials, Depends(data_can_be_accessed)],
    db: Session = Depends(get_db),
):
    result = []
    for song in crud.get_songs(db):
        links = schemas.Links(self=schemas.Link(href=f"{BASE_URL}v1/songs/{song.id}"))
        result.append(schemas.Song(**song.to_dict(), links=links))

    return result


@app.put("/v1/songs/{song_id}")
def update_song(
    song_id: int,
    song: schemas.SongCreate,
    _: Annotated[HTTPBasicCredentials, Depends(data_can_be_accessed)],
    db: Session = Depends(get_db),
):
    db_song = crud.update_song(db, song_id=song_id, song=song)
    print("Song updated.", db_song)
    links = schemas.Links(self=schemas.Link(href=f"{BASE_URL}v1/songs/{song_id}"))
    return schemas.Song(**db_song.to_dict(), links=links)


@app.delete("/v1/songs/{song_id}")
def delete_song(
    song_id: int,
    _: Annotated[HTTPBasicCredentials, Depends(data_can_be_accessed)],
    db: Session = Depends(get_db),
):
    db_song = crud.get_song_by_id(db, song_id=song_id)
    if db_song is None:
        raise HTTPException(status_code=400, detail="Song doesn't exist")

    crud.delete_song_by_id(db=db, song_id=song_id)
    return {"details": "Deleted song."}
