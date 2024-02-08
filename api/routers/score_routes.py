from typing import List

from fastapi import Depends, APIRouter

from auth_management.auth import auth_exc, get_current_active_user
from db_management.models.entities import Score, User
from services.controllers import score_controller

score_router = APIRouter(
    responses={404: {"description": "not found"}})


@score_router.post("/", response_model=str)
async def create_score(current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise auth_exc
    return await score_controller.create_score(current_user.id)


@score_router.get("/", response_model=Score | None)
async def get_user_score(current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise auth_exc
    return await score_controller.get_user_score(current_user.id)


@score_router.put("/{user_id}", response_model=bool | None)
async def update_score(user_id: str,  activity: str,
                       current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise auth_exc
    return await score_controller.update_score(user_id, activity)
