from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from ..utils.mongodb import get_database
from ..models.responses import UsersInResponse, UserInResponse
from ..models.user import User

router = APIRouter()


@router.get("/", response_model=UsersInResponse)
async def get_all_users(db: AsyncIOMotorClient = Depends(get_database)) -> UsersInResponse:
    """Get all data base Users"""
    users = [User(**data) async for data in db['core']['users'].find()]
    return UsersInResponse(data=users)


@router.post('/', response_model=UserInResponse)
async def add_user(user: User, db: AsyncIOMotorClient = Depends(get_database)) -> UserInResponse:
    """Add user to db"""
    user_dict = user.dict()
    user_dict.pop('id')
    _res = await db['core']['users'].insert_one(user_dict)
    user.id = _res.inserted_id
    print(_res)

    return user
