from typing import List

from bson import ObjectId
from pydantic import json, EmailStr

from db_management.db_connection import users_collection
from db_management.models.entities import User, UserDTO


async def create_user(user: User) -> str:
    user_data = user.to_dict()
    result = users_collection.insert_one(user_data)
    return str(result.inserted_id)


async def get_all_users() -> List[UserDTO]:
    return [UserDTO.from_dict(user) for user in users_collection.find()]


async def get_user(user_id: ObjectId) -> UserDTO:
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    return UserDTO.from_dict(user_data) if user_data else None


async def update_user(user_id: ObjectId, updated_user: User) -> bool:
    result = users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user.to_dict()})
    return result.modified_count > 0


async def delete_user(user_id: ObjectId) -> bool:
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    return result.deleted_count > 0


async def user_verification(email: EmailStr) -> User:
    user_data = users_collection.find_one({'email': email})
    return User.from_dict(user_data) if user_data else None