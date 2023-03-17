import asyncio

from typing import Generator
from db import Base, get_session
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine

from main import app
from config import settings


postgres_url = (
    f"postgresql+asyncpg://{settings.TEST_POSTGRES_USER}:{settings.TEST_POSTGRES_PASSWORD}@"
    f"{settings.TEST_POSTGRES_HOST}:{settings.TEST_POSTGRES_PORT}/{settings.TEST_POSTGRES_DB}"
)

async_engine = create_async_engine(
   postgres_url,
   echo=True,
   future=True
)

db_session = async_scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=async_engine,
        class_=AsyncSession,
    ),
    scopefunc=asyncio.current_task,
    )


async def overrided_db():
    async with db_session() as session:
       async with async_engine.begin() as conn:
           await conn.run_sync(Base.metadata.create_all)
       yield session


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
   loop = asyncio.get_event_loop_policy().new_event_loop()
   yield loop
   loop.close()
   
   
@pytest_asyncio.fixture
async def async_client():
    app.dependency_overrides[get_session] = overrided_db
    async with AsyncClient(app=app, base_url='http://localhost') as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
   async with db_session() as session:
       async with async_engine.begin() as conn:
           await conn.run_sync(Base.metadata.create_all)
       yield session

   async with async_engine.begin() as conn:
       await conn.run_sync(Base.metadata.drop_all)

   await async_engine.dispose()


@pytest_asyncio.fixture
async def test_data() -> list:
    bet1 = dict(event_id=2, coefficient=2.44, price=5600)
    bet2 = dict(event_id=3, coefficient=3.66, price=47000)
    bet3 = dict(event_id=3, coefficient=1.67, price=5900)
    return [bet1, bet2, bet3]
