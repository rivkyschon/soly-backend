from typing import Union
import re

from pydantic import BaseModel, EmailStr, field_validator


class EmailVerification(BaseModel):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[EmailStr, None] = None


class Auth_User(BaseModel):
    password: Union[str, None] = None
    disabled: Union[bool, None] = None
    email: Union[EmailStr, None] = None
    is_admin: bool = False

    @field_validator('password')
    def validate_password_strength(cls, password: str) -> str:
        if password is not None:
            pattern = (
                r'^(?=.*[a-z])'  # at least one lowercase letter
                r'(?=.*[A-Z])'  # at least one uppercase letter
                r'(?=.*\d)'  # at least one digit
                # r'(?=.*[@_!#$%^&*()<>?/\|}{~:])'  # at least one special character (commented out)
                r'.{8,}$'  # at least 8 characters total
            )
            if not re.match(pattern, password):
                raise ValueError('Password does not meet strength requirements')
        return password
