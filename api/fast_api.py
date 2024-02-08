# import sys
# from pathlib import Path
#
# import uvicorn
#
# from api.routers.resource_routes import resource_router
#
# sys.path.append(str(Path(__file__).resolve().parent))
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
#
# from routers.chat_routes import chats_router
# from routers.conversation_routes import conversation_router
# from routers.user_routes import users_router
# from routers.auth_routes import auth_router
# from routers.score_routes import score_router
#
# app = FastAPI()
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(users_router, prefix="/users", tags=["users"])
# app.include_router(chats_router, prefix="/chats", tags=['chats'])
# app.include_router(conversation_router, prefix="/conversations", tags=['conversations'])
# app.include_router(resource_router, prefix="/resources", tags=['resources'])
# app.include_router(score_router, prefix="/scores", tags=['scores'])
#
#
# @app.get("/")
# async def test():
#     """
#     This is a test route for the meantime.
#     """
#     return '🤔'
#
#
# '''
# run in terminal:
# uvicorn api.fast_api:app --reload
# '''
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
#
import sys
from pathlib import Path

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.resource_routes import resource_router
from routers.chat_routes import chats_router
from routers.conversation_routes import conversation_router
from routers.user_routes import users_router
from routers.auth_routes import auth_router
from routers.score_routes import score_router

app = FastAPI()

# Define the origins for CORS
origins = [
    "http://localhost",
    "http://localhost:19006",  # Replace with your React Native app's origin
    "http://127.0.0.1",
    "http://127.0.0.1:19006",  # Replace with your React Native app's origin
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Adjust as needed
    allow_headers=["*"],  # Adjust as needed
)

# Include your routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(chats_router, prefix="/chats", tags=['chats'])
app.include_router(conversation_router, prefix="/conversations", tags=['conversations'])
app.include_router(resource_router, prefix="/resources", tags=['resources'])
app.include_router(score_router, prefix="/scores", tags=['scores'])


@app.get("/")
async def test():
    """
    This is a test route for the meantime.
    uvicorn api.fast_api:app --reload
    """
    return '🤔'


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
