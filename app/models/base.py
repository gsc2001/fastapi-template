from datetime import datetime

from pydantic import BaseModel, BaseConfig
from fastapi import HTTPException
from bson.objectid import ObjectId


class ObjectID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(str(v)):
            raise HTTPException(status_code=400, detail=f'Not a valid ID {v}')
        return ObjectId(str(v))


class Base(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        arbitary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.replace(
                tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
            ObjectId: ObjectID
        }
