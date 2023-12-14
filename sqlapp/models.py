from sqlalchemy import Column, ForeignKey, Integer, String

from sqlapp.database import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    artist = Column(String, index=True)
    url = Column(String, index=True)
    platform = Column(String, index=True)
    shared_by = Column(String, nullable=True, index=True)
