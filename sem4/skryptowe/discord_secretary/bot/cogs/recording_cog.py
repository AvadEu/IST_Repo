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

VOICE_CONNECT_TIMEOUT = 30.0


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

    @record.error
    async def record_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        # ostatnia linia obrony — żaden wyjątek nie powinien wisieć jako
        # "Ignoring exception in command 'record'"
        logger.exception("Nieobsłużony błąd w komendzie /record", exc_info=error)
        msg = "❌ Wystąpił błąd podczas obsługi nagrywania."
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)

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

        # łączenie z głosem może trwać dłużej niż 3 s (limit odpowiedzi
        # na interakcję) — najpierw defer, potem followup
        await interaction.response.defer()
        channel = voice_state.channel

        try:
            # reconnect=False: nie wpadaj w pętlę ponawiania przy odrzuceniu
            # połączenia (np. close code 4017 — wymagane E2EE/DAVE)
            vc = await channel.connect(
                cls=voice_recv.VoiceRecvClient,
                timeout=VOICE_CONNECT_TIMEOUT,
                reconnect=False,
            )
        except Exception:
            logger.exception("Nie udało się połączyć z kanałem głosowym")
            await self._safe_disconnect(interaction.guild)
            await interaction.followup.send(
                "❌ Nie udało się połączyć z kanałem głosowym.", ephemeral=True
            )
            return

        wav_path = os.path.join(settings.audio_dir, f"{uuid.uuid4()}.wav")
        try:
            vc.listen(voice_recv.WaveSink(wav_path))
        except Exception:
            logger.exception("Nie udało się rozpocząć nagrywania")
            await self._safe_disconnect(interaction.guild, vc)
            await interaction.followup.send(
                "❌ Nie udało się rozpocząć nagrywania.", ephemeral=True
            )
            return

        self.sessions[interaction.guild_id] = RecordingSession(
            vc=vc,
            wav_path=wav_path,
            channel_id=str(channel.id),
            recorded_by=str(interaction.user.id),
            text_channel=interaction.channel,
        )
        await interaction.followup.send("🔴 Nagrywanie rozpoczęte.")

    async def _stop(self, interaction: discord.Interaction):
        session = self.sessions.pop(interaction.guild_id, None)
        if session is None:
            await interaction.response.send_message(
                "Brak aktywnego nagrywania.", ephemeral=True
            )
            return

        await interaction.response.defer()

        # zatrzymaj odbiór audio i rozłącz — WaveSink finalizuje plik .wav
        try:
            session.vc.stop_listening()
        except Exception:
            logger.exception("Błąd przy stop_listening")
        try:
            await session.vc.disconnect()
        except Exception:
            logger.exception("Błąd przy rozłączaniu z głosem")

        try:
            recording = await self._finalize(session)
        except Exception:
            logger.exception("Nie udało się zapisać nagrania")
            self._cleanup_file(session.wav_path)
            await interaction.followup.send(
                "❌ Nie udało się zapisać nagrania (możliwe, że nie odebrano "
                "poprawnego dźwięku).",
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            f"✅ Nagranie zapisane (#{recording.id}). "
            f"Panel webowy: http://localhost:{settings.web_port}/recordings"
        )

    async def _finalize(self, session: RecordingSession):
        """Konwertuje nagrany .wav na .ogg i zapisuje rekord w bazie."""
        if not os.path.exists(session.wav_path) or os.path.getsize(session.wav_path) == 0:
            raise ValueError("brak danych audio do zapisania")

        ogg_path = os.path.join(settings.audio_dir, f"{uuid.uuid4()}.ogg")
        audio = AudioSegment.from_wav(session.wav_path)
        audio.export(ogg_path, format="ogg")
        self._cleanup_file(session.wav_path)

        async with AsyncSessionLocal() as db:
            return await recording_service.save_recording(
                db,
                file_path=ogg_path,
                channel_id=session.channel_id,
                recorded_by=session.recorded_by,
            )

    async def _safe_disconnect(self, guild, vc=None):
        """Rozłącza ewentualne wiszące połączenie głosowe na serwerze."""
        vc = vc or (guild.voice_client if guild else None)
        if vc is not None:
            try:
                await vc.disconnect(force=True)
            except Exception:
                logger.exception("Błąd przy awaryjnym rozłączaniu z głosem")

    @staticmethod
    def _cleanup_file(path: str):
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                logger.exception("Nie udało się usunąć pliku tymczasowego %s", path)


async def setup(bot: commands.Bot):
    await bot.add_cog(RecordingCog(bot))
