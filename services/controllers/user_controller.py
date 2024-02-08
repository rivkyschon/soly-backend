from bson import ObjectId
from datetime import datetime, date

from db_management.entities_CRUD import user_CRUD
from db_management.models.entities import User, UserDTO, Score
from services.controllers.score_controller import create_score
from db_management.entities_CRUD import score_CRUD


async def create_user(user: User) -> str:
    # await create_score(user.id)
    return await user_CRUD.create_user(user)


async def get_user(user_id: str) -> UserDTO:
    return await user_CRUD.get_user(ObjectId(user_id))


async def get_all_users() -> list[UserDTO]:
    return await user_CRUD.get_all_users()


async def update_user(user_id: str, updated_user: User) -> bool:
    return await user_CRUD.update_user(ObjectId(user_id), updated_user)


async def delete_user(user_id: str) -> bool:
    return await user_CRUD.delete_user(ObjectId(user_id))
