from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Meeting, Reminder

VALID_TARGET_TYPES = {"user", "role"}


async def create_reminder(
    db: AsyncSession,
    meeting_id: int,
    target_type: str,
    target_id: str,
    remind_at: datetime,
    message: str,
) -> Reminder:
    if target_type not in VALID_TARGET_TYPES:
        raise ValueError('target_type must be "user" or "role"')

    meeting = await db.get(Meeting, meeting_id)
    if meeting is None:
        raise ValueError(f"meeting {meeting_id} does not exist")
    if remind_at >= meeting.start_time:
        raise ValueError("remind_at must be before meeting.start_time")

    reminder = Reminder(
        meeting_id=meeting_id,
        target_type=target_type,
        target_id=target_id,
        remind_at=remind_at,
        message=message,
        sent=False,
    )
    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)
    return reminder


async def update_reminder_time(
    db: AsyncSession, reminder_id: int, remind_at: datetime
) -> Reminder | None:
    reminder = await db.get(Reminder, reminder_id)
    if reminder is None:
        return None

    meeting = await db.get(Meeting, reminder.meeting_id)
    if meeting is not None and remind_at >= meeting.start_time:
        raise ValueError("remind_at must be before meeting.start_time")

    reminder.remind_at = remind_at
    # po zmianie czasu przypomnienie ma zostać wysłane ponownie o nowej porze
    reminder.sent = False
    reminder.sent_at = None
    await db.commit()
    await db.refresh(reminder)
    return reminder


async def get_pending_reminders(db: AsyncSession) -> list[Reminder]:
    stmt = select(Reminder).where(
        Reminder.sent.is_(False),
        Reminder.remind_at <= datetime.now(),
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def mark_sent(db: AsyncSession, reminder_id: int) -> None:
    reminder = await db.get(Reminder, reminder_id)
    if reminder is None:
        return
    reminder.sent = True
    reminder.sent_at = datetime.now()
    await db.commit()


async def get_reminders_for_meeting(
    db: AsyncSession, meeting_id: int
) -> list[Reminder]:
    stmt = (
        select(Reminder)
        .where(Reminder.meeting_id == meeting_id)
        .order_by(Reminder.remind_at)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())
