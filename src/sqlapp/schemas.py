from pydantic import BaseModel, HttpUrl


class Link(BaseModel):
    href: HttpUrl


class Links(BaseModel):
    self: Link
    type: str = "GET"


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
    links: Links

    class Config:
        orm_mode = True
