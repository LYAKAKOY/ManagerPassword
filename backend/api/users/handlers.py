from logging import getLogger
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.schemas import ShowUser, CreateUser, UpdateUser
from db.session import get_db
from api.actions.user import _create_user, _update_user_password, _get_user_by_login

user_router = APIRouter()

logger = getLogger(__name__)


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
