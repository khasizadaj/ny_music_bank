from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sqlapp import crud, models, schemas
from sqlapp.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO Have better structured API endpoints
@app.post("/v1/songs/", response_model=schemas.Song)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_details(db,
                                       artist=song.artist,
                                       name=song.name,
                                       url=song.url)
    if db_song:
        raise HTTPException(status_code=400, detail="Song already exists.")

    return crud.create_song(db, song=song)


@app.get("/v1/songs/{song_id}", response_model=schemas.Song)
def get_song(song_id: int, db: Session = Depends(get_db)):
    return crud.get_song_by_id(db, song_id=song_id)


@app.get("/v1/songs/", response_model=list[schemas.Song])
def get_songs(db: Session = Depends(get_db)):
    return crud.get_songs(db)

