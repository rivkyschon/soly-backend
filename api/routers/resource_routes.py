from typing import List

from fastapi import Depends, APIRouter

from auth_management.auth import auth_exc, get_current_active_user
from db_management.models.entities import Resource, User
from services.controllers import resource_controller

resource_router = APIRouter(
    responses={404: {"description": "not found"}})


@resource_router.post("/", response_model=str)
async def create_resource(resource: Resource, current_user: User = Depends(get_current_active_user)):
    """
        Create a new resource.

        Args:
        - resource (Resource): The resource object to be created.
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - str: A string indicating the result of the resource creation process.
        """
    if not current_user:
        raise auth_exc
    return await resource_controller.create_resource(resource)


@resource_router.get("/", response_model=List[Resource] | None)
async def get_all_resources(current_user: User = Depends(get_current_active_user)):
    """
        Retrieve information for all resources.

        Args:
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - List[Resource]: A list of resource objects representing all the user's resources.
        """
    if not current_user:
        raise auth_exc
    return await resource_controller.get_all_resources(current_user.id)


@resource_router.put("/{resource_id}", response_model=bool | None)
async def update_resource(resource_id: str, updated_resource: Resource, current_user: User = Depends(get_current_active_user)):
    """
        Update a specific resource.

        Args:
        - resource_id (str): The unique identifier of the resource to update.
        - updated_resource (Resource): The updated resource object.
        - current_user (User): The current authenticated user, obtained from dependency.

        Raises:
        - auth_exc: If no current user is authenticated.

        Returns:
        - bool | None: A boolean indicating the result of the resource update process or None if the resource doesn't exist.
        """
    if not current_user:
        raise auth_exc
    return await resource_controller.update_resource(resource_id, updated_resource)


@resource_router.delete("/{resource_id}", response_model=bool)
async def delete_resource(resource_id: str, current_user: User = Depends(get_current_active_user)) -> bool:
    """
    Delete a specific resource.

    Args:
    - resource_id (str): The unique identifier of the resource to delete.
    - current_user (User): The current authenticated user, obtained from dependency.

    Raises:
    - auth_exc: If no current user is authenticated.

    Returns:
    - bool: True if deletion was successful, False otherwise.
    """
    if not current_user:
        raise auth_exc
    return await resource_controller.delete_resource(resource_id)