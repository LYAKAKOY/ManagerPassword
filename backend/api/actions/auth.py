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


async def _get_user_by_login_for_auth(login: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_login(login=login)


async def authenticate_user(
        login: str, password: str, db: AsyncSession
) -> User | None:
    user = await _get_user_by_login_for_auth(login=login, session=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_login_for_auth(login=login, session=db)
    if user is None:
        raise credentials_exception
    return user
