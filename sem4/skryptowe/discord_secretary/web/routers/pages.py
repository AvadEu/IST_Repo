from collections import OrderedDict
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from models.models import Meeting, Reminder
from services import meeting_service, recording_service

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    # panel jest globalny (jak scheduler/przypomnienia) — bez filtra po guild,
    # żeby spotkania z każdego serwera bota były widoczne
    upcoming = await meeting_service.get_meetings(db, upcoming_only=True)
    recordings = await recording_service.get_recordings(db)

    today = datetime.now().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(days=1)
    today_stmt = select(Meeting).where(
        Meeting.start_time >= start, Meeting.start_time < end
    )
    meetings_today = len((await db.execute(today_stmt)).scalars().all())

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "upcoming": upcoming,
            "recordings": recordings,
            "recordings_count": len(recordings),
            "meetings_today": meetings_today,
        },
    )


@router.get("/meetings", response_class=HTMLResponse)
async def meetings_page(request: Request, db: AsyncSession = Depends(get_db)):
    meetings = await meeting_service.get_meetings(db)
    return templates.TemplateResponse(
        request, "meetings.html", {"meetings": meetings}
    )


@router.get("/reminders", response_class=HTMLResponse)
async def reminders_page(request: Request, db: AsyncSession = Depends(get_db)):
    stmt = select(Reminder).order_by(Reminder.meeting_id, Reminder.remind_at)
    reminders = (await db.execute(stmt)).scalars().all()

    grouped: "OrderedDict[int, list[Reminder]]" = OrderedDict()
    for reminder in reminders:
        grouped.setdefault(reminder.meeting_id, []).append(reminder)

    return templates.TemplateResponse(
        request, "reminders.html", {"grouped": grouped}
    )


@router.get("/recordings", response_class=HTMLResponse)
async def recordings_page(request: Request, db: AsyncSession = Depends(get_db)):
    recordings = await recording_service.get_recordings(db)
    return templates.TemplateResponse(
        request, "recordings.html", {"recordings": recordings}
    )
