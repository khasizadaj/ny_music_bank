from pydantic import BaseModel

class SongBase(BaseModel):
    name: str
    artist: str
    url: str
    platform: str
    shared_by: str | None = None

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int

    class Config:
        orm_mode = True