import sys
from pathlib import Path

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine as cae

# Добавляем путь к папке app в sys.path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.models import Base


@pytest_asyncio.fixture
async def db_session():
    engine = cae("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()
        await engine.dispose()