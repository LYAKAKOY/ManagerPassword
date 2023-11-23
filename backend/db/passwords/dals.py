import uuid
from typing import List

from db.passwords.models import Password
from db.users.models import User
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class PasswordDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_password(
        self, user_id: uuid.UUID, service_name: str, password: str
    ) -> Password | None:
        new_password = Password(
            user_id=user_id, service_name=service_name, password=password
        )
        try:
            self.db_session.add(new_password)
            await self.db_session.commit()
            await self.db_session.flush()
            return new_password
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def update_password(
        self, user_id: uuid.UUID, service_name: str, password: str
    ) -> Password | None:
        query = (
            update(Password)
            .where(Password.user_id == user_id, Password.service_name == service_name)
            .values(password=password)
            .returning(Password)
        )
        try:
            res = await self.db_session.execute(query)
            updated_password = res.fetchone()
            await self.db_session.commit()
            if updated_password is not None:
                return updated_password[0]
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def get_password_by_service_name(
        self, user_id: uuid.UUID, service_name: str
    ) -> Password | None:
        query = select(Password).where(
            Password.user_id == user_id, Password.service_name == service_name
        )
        password = await self.db_session.scalar(query)
        if password is not None:
            return password

    async def get_password_by_match_service_name(
        self, user_id: uuid.UUID, service_name: str
    ) -> List[Password] | None:
        query = (
            select(Password)
            .where(Password.user_id == user_id)
            .filter(Password.service_name.contains(service_name))
        )
        passwords = await self.db_session.scalars(query)
        if passwords is not None:
            return passwords

    async def get_all_passwords(self, user_id: uuid.UUID) -> List[Password] | None:
        query = (
            select(User)
            .where(User.user_id == user_id)
            .options(selectinload(User.passwords))
        )
        user = await self.db_session.scalar(query)
        return user.passwords
