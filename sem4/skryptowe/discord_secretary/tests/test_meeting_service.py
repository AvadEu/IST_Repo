from datetime import timedelta

import pytest

from schemas.schemas import MeetingCreate
from services import meeting_service


@pytest.mark.asyncio
async def test_create_meeting(db, sample_meeting_data):
    data = MeetingCreate(**sample_meeting_data)
    meeting = await meeting_service.create_meeting(db, data)

    assert meeting.id is not None
    assert meeting.title == "Sprint planning"
    assert len(meeting.participants) == 2


@pytest.mark.asyncio
async def test_collision_detection(db, sample_meeting_data):
    data = MeetingCreate(**sample_meeting_data)
    await meeting_service.create_meeting(db, data)

    overlapping = sample_meeting_data.copy()
    overlapping["start_time"] = sample_meeting_data["start_time"] + timedelta(minutes=30)
    overlapping["end_time"] = sample_meeting_data["end_time"] + timedelta(minutes=30)
    overlapping["participants"] = []

    with pytest.raises(ValueError, match="already has a meeting"):
        await meeting_service.create_meeting(db, MeetingCreate(**overlapping))


@pytest.mark.asyncio
async def test_start_after_end_raises(db, sample_meeting_data):
    bad = sample_meeting_data.copy()
    bad["end_time"] = sample_meeting_data["start_time"]  # equal → invalid
    bad["participants"] = []
    # pydantic validator rejects end <= start at construction time
    with pytest.raises(ValueError):
        MeetingCreate(**bad)


@pytest.mark.asyncio
async def test_get_meetings_upcoming_only(db, sample_meeting_data):
    future = MeetingCreate(**sample_meeting_data)
    await meeting_service.create_meeting(db, future)

    past = sample_meeting_data.copy()
    past["start_time"] = sample_meeting_data["start_time"].replace(year=2000)
    past["end_time"] = sample_meeting_data["end_time"].replace(year=2000)
    past["channel_id"] = "999"
    past["participants"] = []
    await meeting_service.create_meeting(db, MeetingCreate(**past))

    all_meetings = await meeting_service.get_meetings(db, "987654321")
    upcoming = await meeting_service.get_meetings(
        db, "987654321", upcoming_only=True
    )

    assert len(all_meetings) == 2
    assert len(upcoming) == 1
    assert upcoming[0].channel_id == "123456789"


@pytest.mark.asyncio
async def test_cancel_meeting(db, sample_meeting_data):
    meeting = await meeting_service.create_meeting(
        db, MeetingCreate(**sample_meeting_data)
    )
    assert await meeting_service.cancel_meeting(db, meeting.id) is True
    assert await meeting_service.get_meeting(db, meeting.id) is None
    assert await meeting_service.cancel_meeting(db, 99999) is False
