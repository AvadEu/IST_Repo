import logging
import os
import uuid

import discord
from discord import app_commands
from discord.ext import commands
from pydub import AudioSegment

from config import settings
from db.session import AsyncSessionLocal
from services import recording_service

logger = logging.getLogger(__name__)


class RecordingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connections: dict[int, discord.VoiceClient] = {}  # guild_id → VC

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

        if interaction.guild_id in self.connections:
            await interaction.response.send_message(
                "Nagrywanie już trwa na tym serwerze.", ephemeral=True
            )
            return

        channel = voice_state.channel
        vc = await channel.connect()

        filename = f"{uuid.uuid4()}.ogg"
        filepath = os.path.join(settings.audio_dir, filename)

        vc.start_recording(
            discord.sinks.OggSink(),
            self.finished_callback,
            interaction.channel,
            filepath,
            str(channel.id),
            str(interaction.user.id),
        )
        self.connections[interaction.guild_id] = vc
        await interaction.response.send_message("🔴 Nagrywanie rozpoczęte.")

    async def _stop(self, interaction: discord.Interaction):
        vc = self.connections.pop(interaction.guild_id, None)
        if vc is None:
            await interaction.response.send_message(
                "Brak aktywnego nagrywania.", ephemeral=True
            )
            return

        vc.stop_recording()
        await interaction.response.send_message(
            "⏹️ Nagrywanie zatrzymane, zapisuję..."
        )

    async def finished_callback(
        self,
        sink: "discord.sinks.Sink",
        text_channel: discord.abc.Messageable,
        filepath: str,
        channel_id: str,
        recorded_by: str,
    ):
        """Scala ścieżki audio uczestników i zapisuje nagranie."""
        merged: AudioSegment | None = None
        for audio in sink.audio_data.values():
            segment = AudioSegment.from_ogg(audio.file)
            merged = segment if merged is None else merged.overlay(segment)

        if merged is None:
            await text_channel.send("Brak danych audio do zapisania.")
            await self._disconnect(sink)
            return

        merged.export(filepath, format="ogg")

        async with AsyncSessionLocal() as db:
            recording = await recording_service.save_recording(
                db,
                file_path=filepath,
                channel_id=channel_id,
                recorded_by=recorded_by,
            )

        await self._disconnect(sink)
        await text_channel.send(
            f"✅ Nagranie zapisane (#{recording.id}). "
            f"Panel webowy: http://localhost:{settings.web_port}/recordings"
        )

    @staticmethod
    async def _disconnect(sink: "discord.sinks.Sink"):
        vc = getattr(sink, "vc", None)
        if vc is not None:
            await vc.disconnect()


async def setup(bot: commands.Bot):
    await bot.add_cog(RecordingCog(bot))
