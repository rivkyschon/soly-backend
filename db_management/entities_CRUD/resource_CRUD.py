from bson import ObjectId

from db_management.db_connection import resources_collection
from db_management.models.entities import Resource


async def create_resource(resource: Resource) -> str:
    resource_data = resource.__dict__
    result = resources_collection.insert_one(resource_data)
    return str(result.inserted_id)


async def get_all_resources(user_id: str) -> list[Resource]:
    return [Resource(**resource) for resource in resources_collection.find({'user_id': user_id})]


async def update_resource(resource_id: str, updated_resource: Resource) -> bool:
    result = resources_collection.update_one({'_id': ObjectId(resource_id)}, {'$set': updated_resource.__dict__})
    return result.modified_count > 0


async def delete_resource(resource_id: str) -> bool:
    result = resources_collection.delete_one({'_id': ObjectId(resource_id)})
    return result.deleted_count > 0