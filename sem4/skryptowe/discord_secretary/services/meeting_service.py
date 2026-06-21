from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.models import Meeting, MeetingParticipant
from schemas.schemas import MeetingCreate


async def create_meeting(db: AsyncSession, data: MeetingCreate) -> Meeting:
    if data.start_time >= data.end_time:
        raise ValueError("start_time must be before end_time")

    # collision check: overlapping meeting in the same channel
    overlap_stmt = select(Meeting).where(
        and_(
            Meeting.channel_id == data.channel_id,
            Meeting.start_time < data.end_time,
            Meeting.end_time > data.start_time,
        )
    )
    existing = (await db.execute(overlap_stmt)).scalars().first()
    if existing is not None:
        raise ValueError(
            f"channel {data.channel_id} already has a meeting in this time range"
        )

    meeting = Meeting(
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        channel_id=data.channel_id,
        guild_id=data.guild_id,
        created_by=data.created_by,
    )
    for participant in data.participants:
        meeting.participants.append(
            MeetingParticipant(
                discord_user_id=participant.discord_user_id,
                discord_role_id=participant.discord_role_id,
            )
        )

    db.add(meeting)
    await db.commit()
    # refresh only the server-generated column so the already-loaded
    # participants collection is not expired (avoids lazy-load IO outside
    # the async context)
    await db.refresh(meeting, ["created_at"])
    return meeting


async def get_meetings(
    db: AsyncSession, guild_id: str, upcoming_only: bool = False
) -> list[Meeting]:
    stmt = select(Meeting).where(Meeting.guild_id == guild_id)
    if upcoming_only:
        stmt = stmt.where(Meeting.start_time >= datetime.now())
    stmt = stmt.order_by(Meeting.start_time)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_meeting(db: AsyncSession, meeting_id: int) -> Meeting | None:
    stmt = (
        select(Meeting)
        .where(Meeting.id == meeting_id)
        .options(
            selectinload(Meeting.participants),
            selectinload(Meeting.reminders),
        )
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def cancel_meeting(db: AsyncSession, meeting_id: int) -> bool:
    meeting = await db.get(Meeting, meeting_id)
    if meeting is None:
        return False
    # reminders and participants removed via cascade="all, delete-orphan"
    await db.delete(meeting)
    await db.commit()
    return True
