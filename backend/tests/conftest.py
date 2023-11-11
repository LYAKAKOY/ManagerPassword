import asyncio
import uuid
from typing import Any
from typing import Generator

import asyncpg
import pytest
import settings
from db.session import get_db
from httpx import AsyncClient
from JWT import create_access_token
from main import app
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

test_engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

test_async_session = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

CLEAN_TABLES = ["passwords"]


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def _get_test_db():
    test_db = test_async_session()
    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning}"))


@pytest.fixture(scope="session", autouse=True)
async def clean_table_users(async_session_test):
    """Clean data in users table before running session"""
    async with async_session_test() as session:
        async with session.begin():
            await session.execute(text("TRUNCATE TABLE users CASCADE"))


@pytest.fixture(scope="function")
async def client() -> Generator[AsyncClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `get_db` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    app.dependency_overrides[get_db] = _get_test_db
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def create_user(asyncpg_pool):
    user_id = uuid.uuid4()
    async with asyncpg_pool.acquire() as connection:
        await connection.execute(
            """INSERT INTO users VALUES ($1, $2, $3)""",
            user_id,
            "Lewislogin",
            "password",
        )
        return user_id


@pytest.fixture
async def create_test_auth_headers_for_user(create_user):
    access_token = create_access_token(
        data={"sub": str(create_user), "other_custom_data": []}
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(settings.DATABASE_URL.split("+asyncpg")))
    yield pool
    pool.close()
