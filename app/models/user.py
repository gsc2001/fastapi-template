from typing import List

from pydantic import Field, validator

from .base import Base, ObjectID


class User(Base):
    id: ObjectID = Field(None, alias="_id")
    name: str
    username: str


class UserInDB(User):
    hashed_password: str


class RegisterUser(Base):
    name: str
    username: str
    password: str

    @validator('password')
    def password_length_check(cls, v):
        if len(str(v)) < 6:
            raise ValueError('Password length should be greater that 6')
        return str(v)


class TokenData(Base):
    user_id: ObjectID
    scopes: List[str] = []
