from datetime import datetime, timedelta
from typing import Union, Optional, Dict
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from starlette.websockets import WebSocket
from auth_management.auth_models import TokenData, Auth_User
from db_management.models.entities import User
from db_management.entities_CRUD.user_CRUD import user_verification

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

from fastapi import HTTPException, status
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from typing import Optional


class OAuth2PasswordBearerHeaderOnly(OAuth2):
    def __init__(
            self,
            token_url: str,
            scheme_name: Optional[str] = None,
            auto_error: bool = True
    ):
        flows = OAuthFlowsModel(password={"tokenUrl": token_url})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None

        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None

        return param


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerHeaderOnly(token_url="token")
auth_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized"
)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    newly_hashed = pwd_context.hash(plain_password)
    print("newly password is: ---" + newly_hashed + "--- done")

    return pwd_context.verify(plain_password, hashed_password)


# get user by email
async def get_user(email: str):
    user = await user_verification(email)
    print(user)
    return user


async def authenticate_user(email: str, password: str):
    #     get username and password and needs to check if its exists in db and
    #     if the hash password verify to the password he enters
    user: User = await get_user(email)
    if not user:
        return None
    print("password is: ---" + user.hashed_password + "--- done")
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Auth_User = Depends(get_current_user)):
    if current_user and current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_user_for_ws(token: str) -> User | None:
    """
    WebSocket authentication function to get the current active user based on the provided token.

    Parameters:
    - token: Token obtained from the WebSocket connection

    Returns:
    - User model if authentication is successful, else None
    """
    return await get_current_user(token)
