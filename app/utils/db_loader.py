import logging

from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .mongodb import db


async def connect_db():
    """Connect to db on start up
    """
    logging.debug('Connecting to a database client')
    db.client = AsyncIOMotorClient(
        DATABASE_URL, maxPoolSize=MAX_CONNECTIONS_COUNT, minPoolSize=MIN_CONNECTIONS_COUNT)


async def disconnect_db():
    """Disconnect from db
    """
    logging.debug('Disconnection from db')
    db.client.close()
