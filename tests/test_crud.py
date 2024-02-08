from bson import ObjectId

from auth_management.auth import validate_password_strength
from db_management.entities_CRUD.conversation_CRUD import create_conversation, get_conversation_by_id
from db_management.entities_CRUD.message_CRUD import create_massage
from db_management.models.entities import Message, Conversation


async def test_create_massage():
    message = Message(
        id="123",  # Replace '...' with the actual ObjectId
        conversation_id="456",  # Replace '...' with the actual ObjectId
        content="Hello, world!",
        attachment=None  # Provide the actual attachment if needed
    )

    res = await create_massage(message)
    print("res: ", res)


async def test_create_conversation():
    conversation = Conversation(
        id="214256190",
        user_id="657dfb859d368a026b7d0c7d",
        title="Conversation 1",
        massage_lst=[],
        is_shown=True
    )
    res = await create_conversation(conversation)
    print(res)


async def test_get_conversation_by_id():
    res = await get_conversation_by_id(ObjectId('657ec4f09600c7509883dd11'))
    print("res ", res)


# asyncio.run(test_get_conversation_by_id())

def test_validate_password_strength():
    password = '123ABHbubjBHVY87'
    assert validate_password_strength(password)
