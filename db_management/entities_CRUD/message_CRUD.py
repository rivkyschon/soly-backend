
from db_management.db_connection import message_collection
from db_management.models.entities import Message


async def create_massage(message: Message):
    return message_collection.insert_one(message.__dict__)


