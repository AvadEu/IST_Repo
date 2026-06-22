import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from config import settings
from db.session import Base, get_db
import models.models  # noqa: F401
from web.app import app


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()


def _meeting_payload(**overrides):
    payload = {
        "title": "Standup",
        "description": "Codzienny standup",
        "start_time": "2030-06-15T14:00:00",
        "end_time": "2030-06-15T14:30:00",
        "channel_id": "123",
        # endpoint listujący filtruje po settings.discord_guild_id —
        # użyj tej samej wartości, żeby test był niezależny od .env
        "guild_id": settings.discord_guild_id,
        "created_by": "web",
    }
    payload.update(overrides)
    return payload


@pytest.mark.asyncio
async def test_get_meetings_empty(client):
    res = await client.get("/api/meetings")
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_post_meeting_creates(client):
    res = await client.post("/api/meetings", json=_meeting_payload())
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Standup"
    assert body["id"] is not None

    listing = await client.get("/api/meetings")
    assert len(listing.json()) == 1


@pytest.mark.asyncio
async def test_post_meeting_without_end_defaults(client):
    payload = _meeting_payload()
    del payload["end_time"]
    res = await client.post("/api/meetings", json=payload)
    assert res.status_code == 201
    # start 14:00 -> domyślny koniec 15:00 (60 min)
    assert res.json()["end_time"].startswith("2030-06-15T15:00")


@pytest.mark.asyncio
async def test_post_meeting_invalid_times(client):
    bad = _meeting_payload(end_time="2030-06-15T13:00:00")
    res = await client.post("/api/meetings", json=bad)
    assert res.status_code == 422  # pydantic validator rejects end <= start


@pytest.mark.asyncio
async def test_delete_meeting(client):
    created = await client.post("/api/meetings", json=_meeting_payload())
    meeting_id = created.json()["id"]

    res = await client.delete(f"/api/meetings/{meeting_id}")
    assert res.status_code == 200
    assert res.json() == {"ok": True}

    missing = await client.delete(f"/api/meetings/{meeting_id}")
    assert missing.status_code == 404


@pytest.mark.asyncio
async def test_get_recordings_empty(client):
    res = await client.get("/api/recordings")
    assert res.status_code == 200
    assert res.json() == []
