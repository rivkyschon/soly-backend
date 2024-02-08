from datetime import datetime, date

from bson import ObjectId

from auth_management.auth_models import Auth_User

from typing import List, Union
from enum import Enum
from pydantic import BaseModel, EmailStr, constr, HttpUrl, validator, ValidationError, Field


# Enum
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "I don't want to specify"


class Score(BaseModel):
    id: Union[str | None] = None
    user_id: Union[str | None] = None
    total_score: Union[int | None] = None
    level: Union[int | None] = None
    rank_earned: Union[str | None] = None
    streak_days: Union[int | None] = None
    resource_streak_days: Union[int | None] = None
    resources_created: Union[int | None] = None
    last_activity_date: datetime = datetime(1, 1, 1)
    last_resource_creation_date: datetime = datetime(1, 1, 1)


class User(Auth_User):
    id: Union[str | None] = None
    hashed_password: Union[constr(max_length=100), None] = None
    first_name: Union[str | None] = None
    last_name: Union[str | None] = None
    nickname: Union[str, None] = None
    phone_number: Union[str | None] = None
    age: Union[int | None] = None
    gender: Union[GenderEnum | None] = None
    join_date: datetime = Field(default_factory=datetime.now)
    profile_picture: Union[HttpUrl, bytes, None] = None
    in_research: Union[bool | None] = False
    score_id: Union[str, None] = None

    @classmethod
    def from_dict(cls, user_dict):
        user = cls(**user_dict)
        user.id = str(user_dict.get('_id'))
        return user

    def to_dict(self):
        # Copy the dictionary to avoid modifying the original __dict__
        user_data = self.__dict__.copy()
        user_data.pop('password', None)
        return user_data


class UserDTO(BaseModel):
    id: Union[str | None] = None
    email: Union[EmailStr, None] = None
    first_name: Union[str | None] = None
    last_name: Union[str | None] = None
    nickname: Union[str, None] = None
    phone_number: Union[str | None] = None
    age: Union[int | None] = None
    gender: Union[GenderEnum | None] = None
    join_date: datetime = Field(default_factory=datetime.now)
    profile_picture: Union[HttpUrl, bytes, None] = None

    @classmethod
    def from_dict(cls, user_dict):
        user = cls(**user_dict)
        return user

    def to_dict(self):
        return self.__dict__


class Message(BaseModel):
    _id: Union[str | None] = None
    conversation_id: str
    content: str
    sent_datetime: datetime = Field(default_factory=datetime.now)

    # attachment: object  # todo: check which files we have to support

    def to_dict(self):
        # Copy the dictionary to avoid modifying the original __dict__
        user_data = self.__dict__.copy()

        # Convert datetime to ISO 8601 string format
        if isinstance(user_data['sent_datetime'], datetime):
            user_data['sent_datetime'] = user_data['sent_datetime'].isoformat()

        return user_data

    @classmethod
    def from_dict(cls, message_dict):
        message = cls(**message_dict)
        return message


class Conversation(BaseModel):
    _id: Union[str | None] = None
    user_id: str
    create_datetime: datetime = Field(default_factory=datetime.now)
    title: str
    is_shown: Union[bool | None] = True

    def to_dict(self):
        # Copy the dictionary to avoid modifying the original __dict__
        user_data = self.__dict__.copy()
        # Convert user_id to ObjectId type
        return user_data

    @classmethod
    def from_dict(cls, conversation_dict):
        conversation = cls(**conversation_dict)
        return conversation


class Chat(BaseModel):
    message_lst: List[Message]
    user_id: str
    title: str
    create_datetime: datetime = Field(default_factory=datetime.now)


class Resource(BaseModel):
    _id: Union[str | None] = None
    user_id: str
    title: str
    description: str
    create_datetime: datetime = Field(default_factory=datetime.now)
    image: Union[HttpUrl, bytes, None] = None
