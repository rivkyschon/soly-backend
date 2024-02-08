import os

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends

from auth_management.auth import get_current_active_user, auth_exc

from auth_management.auth import get_current_active_user
from db_management.models.entities import User
from soly_chatbot.appendices.attachment import videos_attached

attachment_router = APIRouter(
    responses={404: {"description": "not found"}})


@attachment_router.get("/video/{video_key}", response_class=FileResponse)
async def get_video(video_key: str, current_user: User = Depends(get_current_active_user)):
    """
    Retrieve a video attachment.
    Args:
        video_key:
        current_user:

    Returns:

    """
    if not current_user:
        raise auth_exc
    # Check if the video exists in the dictionary
    if video_key in videos_attached:
        video_path = videos_attached[video_key]
        video_path = "../../" + video_path
        return FileResponse(video_path)
    else:
        raise HTTPException(status_code=404, detail="Video not found")
