import json

from fastapi import APIRouter, WebSocketException
from services.controllers import chat_controller
from db_management.models.entities import Message
from auth_management.auth import get_current_active_user_for_ws
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from queue import Queue
import asyncio
from concurrent.futures import ThreadPoolExecutor
import traceback

from soly_chatbot.chat import Chat

# Constants for queue management
BATCH_SIZE = 50  # Number of messages to process in each batch
PROCESS_INTERVAL = 20  # Time interval (in seconds) for processing messages

# Creating a message queue for temporary message storage
message_queue = Queue()

# ThreadPoolExecutor for handling database writes concurrently
executor = ThreadPoolExecutor(max_workers=10)


async def save_messages(messages):
    """
    Save a batch of messages to the database.
    This function is run in the background to perform database operations.

    Args:
    messages (list): List of messages to be saved.
    """
    try:
        await chat_controller.insert_massage(messages)
    except Exception as e:
        print(f"Error saving messages: {e}")
        traceback.print_exc()


async def process_message_queue():
    """
    Periodically process and save messages from the queue to the database.
    Runs in an infinite loop with a sleep interval defined by PROCESS_INTERVAL.
    """

    while True:
        if not message_queue.empty():
            messages_to_save = []
            while not message_queue.empty() and len(messages_to_save) < BATCH_SIZE:
                msg = message_queue.get()
                messages_to_save.append(msg)

            if messages_to_save:
                loop = asyncio.get_event_loop()
                loop.create_task(save_messages(messages_to_save))

        await asyncio.sleep(PROCESS_INTERVAL)


# API router for the chats endpoint
chats_router = APIRouter(
    responses={404: {"description": "Not found"}}
)


@chats_router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for handling chat messages.
    Authenticates the user and then enters a loop to receive and send messages.

    Args:
    websocket (WebSocket): The WebSocket connection object.
    """
    try:
        await websocket.accept()
    #     # Authentication
    #     token = websocket.headers.get("token")
    #     current_user = await get_current_active_user_for_ws(token)
    except HTTPException as e:
        raise WebSocketException(code=e.status_code, reason=e.detail)

    # Start the message queue processor if not already running
    if not hasattr(websocket_endpoint, "_queue_processor_started"):
        asyncio.create_task(process_message_queue())
        websocket_endpoint._queue_processor_started = True

    soly_chat: Chat = Chat(conversation_id="1", user_id="1")

    while True:
        data = await websocket.receive_json()
        print(data)  # You can still print the entire received JSON for debugging.

        # Assuming your Message model or the incoming JSON directly has conversation_id and user_id
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id')

        # Check if conversation_id and user_id are not None
        if conversation_id is None or user_id is None:
            # Handle cases where conversation_id or user_id is missing
            # For example, you can send an error message back or skip processing this message
            continue  # Or any other error handling

        # If you need to create or update the Chat object with these IDs
        if soly_chat.conversation_id is None:
            soly_chat.conversation_id = conversation_id
        if soly_chat.user_id is None:
            soly_chat.user_id = user_id

        user_message = Message(conversation_id=conversation_id, user_id=user_id, content=data.get('content'))
        soly_message: Message = await soly_chat.get_response(user_message.content)  # Adjust based on your needs

        await websocket.send_json(soly_message.to_dict())

        # Add messages to the queue if needed
        message_queue.put(soly_message)
        message_queue.put(user_message)

    # except WebSocketDisconnect:
    # # Handle WebSocket disconnection
    # pass
