from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from db.session import AsyncSessionLocal
from schemas.schemas import MeetingCreate
from services import meeting_service

DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def _parse_dt(value: str) -> datetime:
    return datetime.strptime(value.strip(), DATETIME_FORMAT)


class MeetingsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    group = app_commands.Group(name="meeting", description="Zarządzanie spotkaniami")

    @group.command(name="create", description="Zaplanuj nowe spotkanie")
    @app_commands.describe(
        title="Tytuł spotkania",
        start="Początek, format: 2025-06-15 14:00",
        end="Koniec, format: 2025-06-15 15:00",
        channel="Kanał głosowy (opcjonalnie)",
        description="Opis (opcjonalnie)",
    )
    async def create(
        self,
        interaction: discord.Interaction,
        title: str,
        start: str,
        end: str,
        channel: discord.VoiceChannel | None = None,
        description: str | None = None,
    ):
        try:
            start_dt = _parse_dt(start)
            end_dt = _parse_dt(end)
        except ValueError:
            await interaction.response.send_message(
                "Niepoprawny format daty. Użyj: 2025-06-15 14:00", ephemeral=True
            )
            return

        channel_id = str(channel.id) if channel else str(interaction.channel_id)
        data = MeetingCreate(
            title=title,
            description=description,
            start_time=start_dt,
            end_time=end_dt,
            channel_id=channel_id,
            guild_id=str(interaction.guild_id),
            created_by=str(interaction.user.id),
        )

        try:
            async with AsyncSessionLocal() as db:
                meeting = await meeting_service.create_meeting(db, data)
        except ValueError as exc:
            await interaction.response.send_message(f"Błąd: {exc}", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Spotkanie utworzone: {meeting.title}",
            description=meeting.description or "",
            color=discord.Color.green(),
        )
        embed.add_field(name="ID", value=str(meeting.id))
        embed.add_field(
            name="Początek", value=meeting.start_time.strftime(DATETIME_FORMAT)
        )
        embed.add_field(
            name="Koniec", value=meeting.end_time.strftime(DATETIME_FORMAT)
        )
        await interaction.response.send_message(embed=embed)

    @group.command(name="list", description="Lista nadchodzących spotkań")
    async def list_meetings(self, interaction: discord.Interaction):
        async with AsyncSessionLocal() as db:
            meetings = await meeting_service.get_meetings(
                db, str(interaction.guild_id), upcoming_only=True
            )

        if not meetings:
            await interaction.response.send_message("Brak nadchodzących spotkań.")
            return

        embed = discord.Embed(
            title="Nadchodzące spotkania", color=discord.Color.blurple()
        )
        for m in meetings:
            embed.add_field(
                name=f"#{m.id} — {m.title}",
                value=f"{m.start_time.strftime(DATETIME_FORMAT)} → "
                f"{m.end_time.strftime(DATETIME_FORMAT)}",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    @group.command(name="cancel", description="Anuluj spotkanie")
    @app_commands.describe(meeting_id="ID spotkania do anulowania")
    async def cancel(self, interaction: discord.Interaction, meeting_id: int):
        async with AsyncSessionLocal() as db:
            ok = await meeting_service.cancel_meeting(db, meeting_id)

        if ok:
            await interaction.response.send_message(
                f"Spotkanie #{meeting_id} zostało anulowane."
            )
        else:
            await interaction.response.send_message(
                f"Nie znaleziono spotkania #{meeting_id}.", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(MeetingsCog(bot))
