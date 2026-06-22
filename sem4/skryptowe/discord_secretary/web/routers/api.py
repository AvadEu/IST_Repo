from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.session import get_db
from models.models import Reminder
from schemas.schemas import (
    MeetingCreate,
    MeetingRead,
    RecordingRead,
    ReminderRead,
)
from services import meeting_service, recording_service

router = APIRouter()


@router.get("/meetings", response_model=list[MeetingRead])
async def list_meetings(db: AsyncSession = Depends(get_db)):
    return await meeting_service.get_meetings(db, settings.discord_guild_id)


@router.post("/meetings", response_model=MeetingRead, status_code=201)
async def create_meeting(data: MeetingCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await meeting_service.create_meeting(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/meetings/{meeting_id}")
async def cancel_meeting(meeting_id: int, db: AsyncSession = Depends(get_db)):
    ok = await meeting_service.cancel_meeting(db, meeting_id)
    if not ok:
        raise HTTPException(status_code=404, detail="meeting not found")
    return {"ok": True}


@router.get("/reminders", response_model=list[ReminderRead])
async def list_reminders(db: AsyncSession = Depends(get_db)):
    stmt = select(Reminder).order_by(Reminder.meeting_id, Reminder.remind_at)
    return list((await db.execute(stmt)).scalars().all())


@router.get("/recordings", response_model=list[RecordingRead])
async def list_recordings(db: AsyncSession = Depends(get_db)):
    return await recording_service.get_recordings(db)


@router.delete("/recordings/{recording_id}")
async def delete_recording(recording_id: int, db: AsyncSession = Depends(get_db)):
    ok = await recording_service.delete_recording(db, recording_id)
    if not ok:
        raise HTTPException(status_code=404, detail="recording not found")
    return {"ok": True}
