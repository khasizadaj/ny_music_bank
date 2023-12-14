from sqlalchemy.orm import Session

from sqlapp import models, schemas


def get_song_by_id(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id==song_id).first()


def get_song_by_details(db: Session, artist: str, name: str, url: str):
    return db.query(models.Song).filter(
        models.Song.artist==artist,
        models.Song.name==name,
        models.Song.url==url
    ).first()


def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()


def create_song(db: Session, song: schemas.SongCreate):
    db_item = models.Song(**song.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
