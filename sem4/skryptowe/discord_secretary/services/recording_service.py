import os

from pydub import AudioSegment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Recording


async def save_recording(
    db: AsyncSession,
    file_path: str,
    channel_id: str,
    recorded_by: str,
    meeting_id: int | None = None,
) -> Recording:
    file_size_bytes = os.path.getsize(file_path)
    audio = AudioSegment.from_ogg(file_path)
    duration_sec = int(audio.duration_seconds)

    recording = Recording(
        meeting_id=meeting_id,
        file_path=file_path,
        original_name=os.path.basename(file_path),
        duration_sec=duration_sec,
        file_size_bytes=file_size_bytes,
        channel_id=channel_id,
        recorded_by=recorded_by,
    )
    db.add(recording)
    await db.commit()
    await db.refresh(recording)
    return recording


async def get_recordings(
    db: AsyncSession, meeting_id: int | None = None
) -> list[Recording]:
    stmt = select(Recording)
    if meeting_id is not None:
        stmt = stmt.where(Recording.meeting_id == meeting_id)
    stmt = stmt.order_by(Recording.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def delete_recording(db: AsyncSession, recording_id: int) -> bool:
    recording = await db.get(Recording, recording_id)
    if recording is None:
        return False

    if os.path.exists(recording.file_path):
        os.remove(recording.file_path)

    await db.delete(recording)
    await db.commit()
    return True
