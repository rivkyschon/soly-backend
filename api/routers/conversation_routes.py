from typing import List

from fastapi import APIRouter, Depends

from auth_management.auth import get_current_active_user, auth_exc
from services.controllers import chat_controller
from db_management.models.entities import User, Conversation, Chat

conversation_router = APIRouter(
    responses={404: {"description": "not found"}})


@conversation_router.get("/", response_model=List[Chat] | List)
async def get_all_users_conversations(current_user: User = Depends(get_current_active_user)):
    """
        Retrieve all conversations for the current user.

        Args:
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - List[Chat]: A list of chat objects representing the user's conversations.
        """
    if not current_user:
        raise auth_exc
    return await chat_controller.get_users_conversations(current_user.id)


@conversation_router.post("/", response_model=str)
async def create_conversation(conversation: Conversation, current_user: User = Depends(get_current_active_user)):
    """
        Create a new conversation.

        Args:
        - conversation (Conversation): The conversation object to be created.
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - str: A string indicating the result of the conversation creation process.
        """
    if not current_user:
        raise auth_exc
    return await chat_controller.create_conversation(conversation)


@conversation_router.delete("/{conversation_id}", response_model=bool)
async def delete_conversation(conversation_id: str, current_user: User = Depends(get_current_active_user)) -> bool:
    """
    Delete a specific conversation.

    Args:
    - conversation_id (str): The unique identifier of the conversation to delete.
    - current_user (User): The current authenticated user, obtained from dependency.

    Raises:
    - auth_exc: If no current user is authenticated.

    Returns:
    - bool: True if deletion was successful, False otherwise.
    """
    if not current_user:
        raise auth_exc
    return await chat_controller.delete_conversation(conversation_id)
