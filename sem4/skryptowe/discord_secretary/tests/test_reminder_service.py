from datetime import datetime, timedelta

import pytest

from schemas.schemas import MeetingCreate
from services import meeting_service, reminder_service


async def _make_meeting(db, sample_meeting_data):
    return await meeting_service.create_meeting(
        db, MeetingCreate(**sample_meeting_data)
    )


@pytest.mark.asyncio
async def test_create_reminder(db, sample_meeting_data):
    meeting = await _make_meeting(db, sample_meeting_data)
    remind_at = meeting.start_time - timedelta(minutes=15)

    reminder = await reminder_service.create_reminder(
        db, meeting.id, "user", "111222333", remind_at, "Spotkanie za 15 min"
    )

    assert reminder.id is not None
    assert reminder.sent is False
    assert reminder.target_type == "user"


@pytest.mark.asyncio
async def test_remind_at_after_start_raises(db, sample_meeting_data):
    meeting = await _make_meeting(db, sample_meeting_data)
    too_late = meeting.start_time + timedelta(minutes=5)

    with pytest.raises(ValueError, match="before meeting.start_time"):
        await reminder_service.create_reminder(
            db, meeting.id, "user", "111", too_late, "spóźnione"
        )


@pytest.mark.asyncio
async def test_invalid_target_type_raises(db, sample_meeting_data):
    meeting = await _make_meeting(db, sample_meeting_data)
    remind_at = meeting.start_time - timedelta(minutes=10)

    with pytest.raises(ValueError, match="user.*role"):
        await reminder_service.create_reminder(
            db, meeting.id, "channel", "111", remind_at, "zła rola"
        )


@pytest.mark.asyncio
async def test_get_pending_reminders(db, sample_meeting_data):
    meeting = await _make_meeting(db, sample_meeting_data)

    # one due (remind_at in the past, not sent)
    due = await reminder_service.create_reminder(
        db, meeting.id, "user", "1", datetime(2000, 1, 1, 12, 0), "due"
    )
    # one in the future (remind_at before meeting start but after now)
    await reminder_service.create_reminder(
        db, meeting.id, "user", "2", meeting.start_time - timedelta(minutes=5), "future"
    )

    pending = await reminder_service.get_pending_reminders(db)
    assert len(pending) == 1
    assert pending[0].id == due.id


@pytest.mark.asyncio
async def test_mark_sent(db, sample_meeting_data):
    meeting = await _make_meeting(db, sample_meeting_data)
    reminder = await reminder_service.create_reminder(
        db, meeting.id, "user", "1", datetime(2000, 1, 1, 12, 0), "due"
    )

    await reminder_service.mark_sent(db, reminder.id)

    pending = await reminder_service.get_pending_reminders(db)
    assert pending == []
    refreshed = await db.get(type(reminder), reminder.id)
    assert refreshed.sent is True
    assert refreshed.sent_at is not None
