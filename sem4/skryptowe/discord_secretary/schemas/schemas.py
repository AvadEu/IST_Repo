from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ParticipantCreate(BaseModel):
    discord_user_id: str | None = None
    discord_role_id: str | None = None


class MeetingCreate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    channel_id: str
    guild_id: str
    created_by: str
    participants: list[ParticipantCreate] = []

    @field_validator("end_time")
    @classmethod
    def end_after_start(cls, v: datetime, info) -> datetime:
        start = info.data.get("start_time")
        if start is not None and v <= start:
            raise ValueError("end_time must be after start_time")
        return v


class MeetingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    channel_id: str
    guild_id: str
    created_by: str
    created_at: datetime


class ReminderCreate(BaseModel):
    meeting_id: int
    remind_at: datetime
    target_type: str
    target_id: str
    message: str


class ReminderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    remind_at: datetime
    target_type: str
    target_id: str
    message: str
    sent: bool
    sent_at: datetime | None


class RecordingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int | None
    file_path: str
    original_name: str
    duration_sec: int | None
    file_size_bytes: int | None
    channel_id: str
    recorded_by: str
    created_at: datetime
