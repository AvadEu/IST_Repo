import logging
import os
import uuid

import discord
from discord import app_commands
from discord.ext import commands, voice_recv
from pydub import AudioSegment

from config import settings
from db.session import AsyncSessionLocal
from services import recording_service

logger = logging.getLogger(__name__)


class RecordingSession:
    def __init__(
        self,
        vc: voice_recv.VoiceRecvClient,
        wav_path: str,
        channel_id: str,
        recorded_by: str,
        text_channel: discord.abc.Messageable,
    ):
        self.vc = vc
        self.wav_path = wav_path
        self.channel_id = channel_id
        self.recorded_by = recorded_by
        self.text_channel = text_channel


class RecordingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sessions: dict[int, RecordingSession] = {}  # guild_id → sesja

    @app_commands.command(
        name="record", description="Nagrywanie kanału głosowego: start lub stop"
    )
    @app_commands.describe(action="start lub stop")
    async def record(self, interaction: discord.Interaction, action: str):
        action = action.lower().strip()
        if action == "start":
            await self._start(interaction)
        elif action == "stop":
            await self._stop(interaction)
        else:
            await interaction.response.send_message(
                'Użyj "start" lub "stop".', ephemeral=True
            )

    async def _start(self, interaction: discord.Interaction):
        voice_state = getattr(interaction.user, "voice", None)
        if voice_state is None or voice_state.channel is None:
            await interaction.response.send_message(
                "Musisz być na kanale głosowym.", ephemeral=True
            )
            return

        if interaction.guild_id in self.sessions:
            await interaction.response.send_message(
                "Nagrywanie już trwa na tym serwerze.", ephemeral=True
            )
            return

        channel = voice_state.channel
        vc = await channel.connect(cls=voice_recv.VoiceRecvClient)

        wav_path = os.path.join(settings.audio_dir, f"{uuid.uuid4()}.wav")
        sink = voice_recv.WaveSink(wav_path)
        vc.listen(sink)

        self.sessions[interaction.guild_id] = RecordingSession(
            vc=vc,
            wav_path=wav_path,
            channel_id=str(channel.id),
            recorded_by=str(interaction.user.id),
            text_channel=interaction.channel,
        )
        await interaction.response.send_message("🔴 Nagrywanie rozpoczęte.")

    async def _stop(self, interaction: discord.Interaction):
        session = self.sessions.pop(interaction.guild_id, None)
        if session is None:
            await interaction.response.send_message(
                "Brak aktywnego nagrywania.", ephemeral=True
            )
            return

        # zatrzymaj odbiór audio i rozłącz — WaveSink finalizuje plik .wav
        session.vc.stop_listening()
        await session.vc.disconnect()
        await interaction.response.send_message(
            "⏹️ Nagrywanie zatrzymane, zapisuję..."
        )

        try:
            recording = await self._finalize(session)
        except Exception:
            logger.exception("Nie udało się zapisać nagrania")
            await session.text_channel.send("❌ Nie udało się zapisać nagrania.")
            return

        await session.text_channel.send(
            f"✅ Nagranie zapisane (#{recording.id}). "
            f"Panel webowy: http://localhost:{settings.web_port}/recordings"
        )

    async def _finalize(self, session: RecordingSession):
        """Konwertuje nagrany .wav na .ogg i zapisuje rekord w bazie."""
        ogg_path = os.path.join(settings.audio_dir, f"{uuid.uuid4()}.ogg")
        audio = AudioSegment.from_wav(session.wav_path)
        audio.export(ogg_path, format="ogg")

        if os.path.exists(session.wav_path):
            os.remove(session.wav_path)

        async with AsyncSessionLocal() as db:
            return await recording_service.save_recording(
                db,
                file_path=ogg_path,
                channel_id=session.channel_id,
                recorded_by=session.recorded_by,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(RecordingCog(bot))
