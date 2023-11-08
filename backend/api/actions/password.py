from typing import List
from crypt import AES
from sqlalchemy.ext.asyncio import AsyncSession
from api.passwords.schemas import ShowPassword
from api.passwords.schemas import CreatePassword
from db.passwords.dals import PasswordDAL
from db.users.models import User


async def _create_or_update_password(service_name: str, body: CreatePassword, current_user: User,
                                     session: AsyncSession) -> ShowPassword | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        if not await password_dal.get_password_by_service_name(user_id=current_user.user_id, service_name=service_name):
            password = await password_dal.create_password(service_name=service_name,
                                                          user_id=current_user.user_id,
                                                          password=AES.encrypt_password(body.password))
        else:
            password = await password_dal.update_password(service_name=service_name,
                                                          user_id=current_user.user_id,
                                                          password=AES.encrypt_password(body.password))
        if password is not None:
            return ShowPassword(
                service_name=password.service_name,
                password=AES.decrypt_password(password.password)
            )


async def _get_password_by_service_name(service_name: str, current_user: User, session: AsyncSession) -> ShowPassword | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        password = await password_dal.get_password_by_service_name(user_id=current_user.user_id, service_name=service_name)
        if password is not None:
            return ShowPassword(
                service_name=password.service_name,
                password=AES.decrypt_password(password.password)
            )


async def _get_passwords_by_match_service_name(service_name: str, current_user: User, session: AsyncSession) -> List[ShowPassword] | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        passwords = await password_dal.get_password_by_match_service_name(user_id=current_user.user_id, service_name=service_name)
        if passwords is not None:
            all_show_passwords = []
            for password in passwords:
                all_show_passwords.append(ShowPassword(
                    service_name=password[0].service_name,
                    password=AES.decrypt_password(password[0].password)
                ))
            return all_show_passwords
