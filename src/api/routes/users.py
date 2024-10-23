"""Users related routes."""
# import logging
# from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm


from src.api.dependencies.database import get_repository
from src.db.repositories.users import UserRepository  
from src.models.users import UserCreate, UserPublic, UserUpdate
from src.services.auth import AuthService
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from src.models.token import AccessToken



users_router = APIRouter()
# audit_logger = logging.getLogger("audit")


# @users_router.post(
#     "/users",
#     response_model=UserPublic,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_user(
#     user_create: UserCreate,
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     """Create a new user."""
#     return await users_repo.create_user(new_user=user_create)


# @users_router.get(
#     "/users/{user_id}",
#     response_model=UserPublic,
#     status_code=status.HTTP_200_OK,
# )
# async def get_user(
#     user_id: UUID,
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     """Get a user by ID."""
#     return await users_repo.get_user_by_id(user_id=user_id)


# @users_router.put(
#     "/users/{user_id}",
#     response_model=UserPublic,
#     status_code=status.HTTP_200_OK,
# )
# async def update_user(
#     user_id: UUID,
#     user_update: UserUpdate,
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     """Update a user."""
#     return await users_repo.update_user(user_id=user_id, user_update=user_update)


# @users_router.delete(
#     "/users/{user_id}",
#     response_model=UserPublic,
#     status_code=status.HTTP_200_OK,
# )
# async def delete_user(
#     user_id: UUID,
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     """Delete a user."""
#     return await users_repo.delete_user(user_id=user_id)


@users_router.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def user_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> AccessToken:
    """Login user."""
    form_data.username = form_data.username.lower()
    token = await user_repo.login(form_data)
    response.set_cookie(
        "access_token",
        value=token.access_token,
        httponly=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        "refresh_token",
        value=token.refresh_token,
        httponly=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return token

@users_router.post(
    "/login/refresh", response_model=AccessToken, status_code=status.HTTP_200_OK
)
async def refresh(
    request: Request,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> AccessToken:
    """Refresh token."""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found"
        )

    return await user_repo.refresh(refresh_token)
users_router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)

@users_router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def signup(
    new_user: UserCreate,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    auth_service: AuthService = Depends(AuthService),
) -> UserPublic:
    """User sign-up route"""

    # Check if the user already exists in the database
    user_in_db = await user_repo.get_user(email=new_user.email)
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = await auth_service.get_password_hash(new_user.password)

    # Create a new user in the database
    created_user = await user_repo.create_user(
        username=new_user.first_name + new_user.last_name,
        email=new_user.email,
        hashed_password=hashed_password
    )

    # Return the public user data (without password)
    return UserPublic(
        id=created_user.id,
        username=created_user.username,
        email=created_user.email,
        created_at=created_user.created_at,
    )