from bson import ObjectId

from db_management.db_connection import scores_collection
from db_management.models.entities import Score


async def create_score(score: Score) -> str:
    score_data = score.__dict__
    result = scores_collection.insert_one(score_data)
    return str(result.inserted_id)


async def get_user_score(user_id: str) -> Score:
    result = scores_collection.find_one({'user_id': user_id})
    return Score(**result)


"""async def update_score(score_id: str, updated_score: Score) -> bool:
    result = scores_collection.update_one({'_id': ObjectId(score_id)}, {'$set': updated_score.__dict__})
    return result.modified_count > 0"""


async def update_score(score_id: str, updated_score: Score) -> bool:
    result = scores_collection.update_one({'id': ObjectId(score_id)}, {'$set': updated_score.__dict__})
    return result.modified_count > 0
