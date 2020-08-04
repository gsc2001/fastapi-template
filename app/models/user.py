from pydantic import Field

from .base import Base, ObjectID


class User(Base):
    id: ObjectID = Field(None, alias="_id")
    name: str
