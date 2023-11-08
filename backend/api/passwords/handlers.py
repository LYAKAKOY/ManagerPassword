from logging import getLogger
from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import get_current_user_from_token
from api.actions.password import _create_or_update_password, _get_password_by_service_name, \
    _get_passwords_by_match_service_name
from api.passwords.schemas import ShowPassword
from api.passwords.schemas import CreatePassword
from db.session import get_db
from db.users.models import User

manager_password_router = APIRouter()

logger = getLogger(__name__)


@manager_password_router.post("/{service_name}", response_model=ShowPassword)
async def create_or_update_password(service_name: str, password: CreatePassword,
                                    current_user: User = Depends(get_current_user_from_token),
                                    db: AsyncSession = Depends(get_db)) -> ShowPassword:
    """Создать или обновить пароль для сервиса"""
    try:
        password = await _create_or_update_password(service_name, password, db)
        if password is None:
            raise HTTPException(
                status_code=500, detail=f"An error occurred try again"
            )
        return password
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@manager_password_router.get("/{service_name}", response_model=ShowPassword)
async def get_password(service_name: str, db: AsyncSession = Depends(get_db)) -> ShowPassword:
    """Получить пароль по заданному сервису"""
    try:
        password = await _get_password_by_service_name(service_name, db)
        if password is None:
            raise HTTPException(
                status_code=404, detail=f"The password of this service not found"
            )
        return password
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@manager_password_router.get("/", response_model=List[ShowPassword])
async def get_passwords_by_match(service_name: str, db: AsyncSession = Depends(get_db)) -> List[ShowPassword]:
    """Получить пароль(и) по части имени сервиса"""
    try:
        passwords = await _get_passwords_by_match_service_name(service_name, db)
        if not passwords:
            raise HTTPException(
                status_code=404, detail=f"No service found"
            )
        return passwords
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
