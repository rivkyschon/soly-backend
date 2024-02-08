from typing import List
from fastapi import APIRouter, Depends
from auth_management.auth import get_current_active_user, auth_exc
from db_management.models.entities import User, UserDTO
from services.controllers import user_controller

users_router = APIRouter(
    responses={404: {"description": "not found"}})


@users_router.get("/current", response_model=UserDTO | None)
async def get_user(current_user: User = Depends(get_current_active_user)):
    """
        Get the current logged-in user's information.

        Args:
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - UserDTO | None: The DTO of the current user or None if no user is logged in.
        """
    if not current_user:
        raise auth_exc
    return UserDTO.from_dict(current_user.to_dict())


@users_router.get("/{user_id}", response_model=UserDTO | None)
async def get_user_by_id(user_id: str, current_user: User = Depends(get_current_active_user)):
    """
        Retrieve a user's information by their ID.

        Args:
        - user_id (str): The unique identifier of the user.
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - UserDTO | None: The DTO of the requested user or None if the user doesn't exist.
        """
    if not current_user:
        raise auth_exc
    return await user_controller.get_user(user_id)


@users_router.get("/", response_model=List[UserDTO] | None)
async def get_all_users(current_user: User = Depends(get_current_active_user)):
    """
        Retrieve information for all users.

        Args:
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - List[UserDTO] | None: A list of DTOs for all users or None if there are no users.
        """
    if not current_user:
        raise auth_exc
    return await user_controller.get_all_users()


@users_router.put("/{user_id}", response_model=bool | None)
async def update_user(user_id: str, updated_user: User, current_user: User = Depends(get_current_active_user)):
    """
        Update a user's information.

        Args:
        - user_id (str): The unique identifier of the user to be updated.
        - updated_user (User): The updated user information.
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - bool | None: True if the update was successful, False otherwise.
        """
    if not current_user:
        raise auth_exc
    return await user_controller.update_user(user_id, updated_user)


@users_router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str, current_user: User = Depends(get_current_active_user)):
    """
       Delete a user by their ID.

       Args:
       - user_id (str): The unique identifier of the user to be deleted.
       - current_user (User): The current authenticated user, obtained from dependency.

       Raises:
       - auth_exc: If no current user is authenticated.

       Returns:
       - dict: A message indicating the success or failure of the deletion process.
       """
    if not current_user:
        raise auth_exc
    deleted_user = await user_controller.delete_user(user_id)
    if deleted_user:
        return {"message": f"User with ID {user_id} deleted successfully"}
    return {"message": f"User with ID {user_id} not found"}
