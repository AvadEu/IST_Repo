from unittest.mock import MagicMock, patch

import pytest

from services import recording_service


@pytest.mark.asyncio
async def test_save_recording(db):
    fake_audio = MagicMock()
    fake_audio.duration_seconds = 42.7

    with patch.object(
        recording_service.os.path, "getsize", return_value=2048
    ), patch.object(
        recording_service.AudioSegment, "from_ogg", return_value=fake_audio
    ):
        recording = await recording_service.save_recording(
            db,
            file_path="/data/audio/abc.ogg",
            channel_id="555",
            recorded_by="111",
        )

    assert recording.id is not None
    assert recording.file_size_bytes == 2048
    assert recording.duration_sec == 42  # truncated int
    assert recording.original_name == "abc.ogg"


@pytest.mark.asyncio
async def test_get_recordings_filter_meeting(db):
    fake_audio = MagicMock()
    fake_audio.duration_seconds = 10.0

    with patch.object(
        recording_service.os.path, "getsize", return_value=100
    ), patch.object(
        recording_service.AudioSegment, "from_ogg", return_value=fake_audio
    ):
        await recording_service.save_recording(
            db, "/data/audio/a.ogg", "1", "1", meeting_id=1
        )
        await recording_service.save_recording(
            db, "/data/audio/b.ogg", "1", "1", meeting_id=2
        )

    all_recs = await recording_service.get_recordings(db)
    only_one = await recording_service.get_recordings(db, meeting_id=1)

    assert len(all_recs) == 2
    assert len(only_one) == 1
    assert only_one[0].meeting_id == 1


@pytest.mark.asyncio
async def test_delete_recording(db):
    fake_audio = MagicMock()
    fake_audio.duration_seconds = 5.0

    with patch.object(
        recording_service.os.path, "getsize", return_value=100
    ), patch.object(
        recording_service.AudioSegment, "from_ogg", return_value=fake_audio
    ):
        recording = await recording_service.save_recording(
            db, "/data/audio/del.ogg", "1", "1"
        )

    with patch.object(
        recording_service.os.path, "exists", return_value=True
    ) as mock_exists, patch.object(
        recording_service.os, "remove"
    ) as mock_remove:
        ok = await recording_service.delete_recording(db, recording.id)

    assert ok is True
    mock_exists.assert_called_once_with("/data/audio/del.ogg")
    mock_remove.assert_called_once_with("/data/audio/del.ogg")
    assert await recording_service.get_recordings(db) == []
    assert await recording_service.delete_recording(db, 99999) is False
