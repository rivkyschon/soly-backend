from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()


client = MongoClient(os.getenv('MONGO_DETAILS'))
db = client[os.getenv('DB_CLIENT')]
users_collection = db['users']
message_collection = db['messages']
conversation_collection = db['conversations']
resources_collection = db['resources']
scores_collection = db['scores']
