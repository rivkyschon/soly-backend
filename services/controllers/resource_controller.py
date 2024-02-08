from db_management.entities_CRUD import resource_CRUD
from db_management.models.entities import Resource


async def create_resource(resource: Resource) -> str:
    return await resource_CRUD.create_resource(resource)


async def get_all_resources(user_id: str) -> list[Resource]:
    return await resource_CRUD.get_all_resources(user_id)


async def update_resource(resource_id: str, updated_resource: Resource) -> bool:
    return await resource_CRUD.update_resource(resource_id, updated_resource)


async def delete_resource(resource_id: str) -> bool:
    return await resource_CRUD.delete_resource(resource_id)
