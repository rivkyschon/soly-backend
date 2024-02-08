from typing import List

from db_management.entities_CRUD import conversation_CRUD
from db_management.models.entities import Message, Conversation, Chat


async def insert_massage(massages: List[Message]):
    return await conversation_CRUD.insert_messages(massages)


async def get_users_conversations(user_id: str) -> List[Chat] | List:
    return await conversation_CRUD.get_users_conversations(user_id)


# async def get_conversation_by_id(conversation_id: ObjectId):
#     return await conversation_CRUD.get_conversation_by_id(conversation_id)


async def create_conversation(conversation: Conversation) -> str:
    return await conversation_CRUD.create_conversation(conversation)


async def delete_conversation(conversation_id: str) -> bool:
    return await conversation_CRUD.delete_conversation(conversation_id)

