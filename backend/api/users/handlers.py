from datetime import timedelta
from logging import getLogger
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import settings
from JWT import create_access_token
from api.actions.auth import authenticate_user
from api.users.schemas import ShowUser, CreateUser, UpdateUser, Token
from db.session import get_db
from api.actions.user import _create_user, _update_user_password

user_router = APIRouter()

logger = getLogger(__name__)


@user_router.post("/login/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "other_custom_data": []},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/auth", response_model=ShowUser)
async def create_user(user: CreateUser,
                      db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Создать пользователя для менеджера паролей"""
    try:
        user = await _create_user(user, db)
        if user is None:
            raise HTTPException(
                status_code=400, detail=f"the login is already occupied"
            )
        return user
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.put("/change_password", response_model=ShowUser)
async def change_password(user_update: UpdateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Получить пароль по заданному сервису"""
    try:
        user = await _update_user_password(user_update, db)
        if user is None:
            raise HTTPException(
                status_code=400, detail=f"The password is too easy"
            )
        return user
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
