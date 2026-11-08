from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import models.models  # noqa: F401  (register tables)
from db.session import Base


@pytest_asyncio.fixture
async def db() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def sample_meeting_data() -> dict:
    start = datetime(2030, 6, 15, 14, 0)
    return {
        "title": "Sprint planning",
        "description": "Planowanie sprintu",
        "start_time": start,
        "end_time": start + timedelta(hours=1),
        "channel_id": "123456789",
        "guild_id": "987654321",
        "created_by": "111222333",
        "participants": [
            {"discord_user_id": "111222333", "discord_role_id": None},
            {"discord_user_id": None, "discord_role_id": "444555666"},
        ],
    }
