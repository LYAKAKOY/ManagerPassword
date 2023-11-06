from logging import getLogger
from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.schemas import ShowUser, CreateUser
from db.session import get_db


user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_or_update_password(user: CreateUser,
                                    db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Создать пользователя для менеджера паролей"""
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


@user_router.put("/{service_name}", response_model=ShowPassword)
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


@user_router.get("/", response_model=List[ShowPassword])
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
