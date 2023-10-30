from typing import Generator, Any
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from main import app
import asyncio
from db.session import get_db
import asyncpg
import settings

test_engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

test_async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False)

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
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False)
    yield async_session

@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning}"))

@pytest.fixture(scope="function")
async def client() -> Generator[AsyncClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `get_db` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    app.dependency_overrides[get_db] = _get_test_db
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as client:
        yield client

@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(settings.DATABASE_URL.split("+asyncpg")))
    yield pool
    pool.close()


@pytest.fixture
async def get_password_from_database(asyncpg_pool):
    async def get_password_from_database_by_service_name(service_name: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM passwords WHERE service_name = $1;""", service_name
            )

    return get_password_from_database_by_service_name