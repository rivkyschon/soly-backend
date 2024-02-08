from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Response, encoders
from fastapi.security import OAuth2PasswordRequestForm

from auth_management.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_password_hash
from auth_management.auth_models import Token, EmailVerification
from services.controllers.user_controller import create_user
from db_management.models.entities import User
from db_management.entities_CRUD.user_CRUD import user_verification
from services.email_service.secure_code_mailer import send_email

# Define the API router for authentication
auth_router = APIRouter(
    responses={404: {"description": "not authenticate"}},
)


@auth_router.post("/token", response_model=Token)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to generate a new authentication token.

    Parameters:
    - response: FastAPI Response object
    - form_data: OAuth2PasswordRequestForm containing username and password

    Returns:
    - JSON response with access token and token type
    """
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    # Set the access token as a cookie in the response
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register", response_model=str)
async def insert_user(user: User):
    """
    Endpoint to register a new user.

    Parameters:
    - user: User model containing user information

    Returns:
    - Response indicating successful user creation
    """
    # Check if the email is already in use
    existing_user = await user_verification(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in user",
        )

    # Hash the password before inserting the user
    user.hashed_password = get_password_hash(user.password)

    # Create the user
    return await create_user(user)


@auth_router.post("/send-verification-email", response_model=int)
async def send_verification_email(user_email: EmailVerification):
    """
    Send a verification email to a user.

    Args:
    - user_email (EmailVerification): An object containing the user's email.

    Raises:
    - Exception: If the user does not exist in the system.

    Returns:
    - int: A verification code sent to the user's email.
    """
    # Verify if the user exists
    if not await user_verification(user_email.email):
        raise Exception('User does not exist')

    # Send verification email and return the verification code
    verification_code = await send_email(user_email.email)
    return verification_code
