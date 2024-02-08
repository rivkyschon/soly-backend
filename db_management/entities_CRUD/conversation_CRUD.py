import asyncio
from typing import List
from bson import ObjectId
from db_management.db_connection import conversation_collection, message_collection
from db_management.models.entities import Conversation, User, UserDTO, Message, Chat


async def get_users_conversations(user_id: str) -> List[Chat]:
    chats = []

    # Find all conversations for the user
    user_conversations = list(conversation_collection.find({'user_id': user_id, "is_shown": True}))
    for conversation in user_conversations:
        # Fetch messages related to this conversation
        messages = list(message_collection.find({'conversation_id': str(conversation['_id'])}))

        # Create the Chat object and add it to the list
        chat = Chat(
            message_lst=[Message.from_dict(message) for message in messages],
            user_id=user_id,
            title=conversation['title'],
            create_datetime=conversation['create_datetime']
        )
        chats.append(chat)

    return chats


#
# async def get_conversation_by_id(conversation_id: ObjectId):
#     return conversation_collection.find_one({"_id": conversation_id})


async def delete_conversation(conversation_id: str) -> bool:
    filter_criteria = {"_id": ObjectId(conversation_id)}
    update_operation = {"$set": {"is_shown": False}}
    result = conversation_collection.update_one(filter_criteria, update_operation)
    return result.modified_count > 0


async def create_conversation(conversation: Conversation) -> str:
    result = conversation_collection.insert_one(conversation.to_dict())
    return str(result.inserted_id)


async def insert_messages(messages: List[Message]):
    messages_dict = [message.to_dict() for message in messages]
    return message_collection.insert_many(messages_dict)
