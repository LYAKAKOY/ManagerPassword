from typing import List
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db.users.models import User


class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, login: str, password: str) -> User | None:
        new_user = User(login=login, password=password)
        try:
            self.db_session.add(new_user)
            await self.db_session.flush()
            await self.db_session.commit()
            return new_user
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def set_password(self, login: str, password: str) -> User | None:
        query = update(User).where(User.login == login).values(password=password).returning(User.user_id)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]

    async def get_user_by_login(self, login: str) -> User | None:
        query = select(User).where(User.login == login).returning(User.user_id)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]