from api.users.schemas import CreateUser, ShowUser, UpdateUser
from sqlalchemy.ext.asyncio import AsyncSession
from db.users.dals import UserDAL
from hashing import Hasher


async def _create_user(body: CreateUser, session) -> ShowUser | None:
    async with session.begin():
        user_dal = UserDAL(session)
        new_user = await user_dal.create_user(login=body.login, password=Hasher.get_password_hash(body.password))
        if new_user is not None:
            return ShowUser(
                user_id=new_user.user_id
            )


async def _update_user_password(body: UpdateUser, session) -> ShowUser | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.set_password(login=body.login, password=body.password)
        if user is not None:
            return ShowUser(
                user_id=user.user_id
            )


async def _get_user_by_login(login: str, session: AsyncSession) -> ShowUser | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_login(login=login)
        if user is not None:
            return ShowUser(
                user_id=user.user_id
            )
