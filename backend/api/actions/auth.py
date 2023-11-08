import uuid

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import settings
from db.session import get_db
from db.users.dals import UserDAL
from db.users.models import User
from hashing import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/token")


async def _get_user_by_user_id_for_auth(user_id: uuid.UUID, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_user_id(user_id=user_id)


async def authenticate_user(
        user_id: uuid.UUID, password: str, db: AsyncSession
) -> User | None:
    user = await _get_user_by_user_id_for_auth(user_id=user_id, session=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.password):
        return
    return user


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_user_id_for_auth(user_id=user_id, session=db)
    if user is None:
        raise credentials_exception
    return user
