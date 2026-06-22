from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from db.session import AsyncSessionLocal
from services import meeting_service, reminder_service

DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class RemindersCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    group = app_commands.Group(name="remind", description="Zarządzanie przypomnieniami")

    @group.command(name="set", description="Ustaw przypomnienie dla usera lub roli")
    @app_commands.describe(
        meeting_id="ID spotkania",
        minutes_before="Ile minut przed spotkaniem wysłać przypomnienie",
        user="Użytkownik do powiadomienia (opcjonalnie)",
        role="Rola do powiadomienia (opcjonalnie)",
        message="Treść wiadomości (opcjonalnie)",
    )
    async def set_reminder(
        self,
        interaction: discord.Interaction,
        meeting_id: int,
        minutes_before: int,
        user: discord.Member | None = None,
        role: discord.Role | None = None,
        message: str | None = None,
    ):
        if (user is None) == (role is None):
            await interaction.response.send_message(
                "Podaj dokładnie jeden cel: użytkownika ALBO rolę.", ephemeral=True
            )
            return

        async with AsyncSessionLocal() as db:
            meeting = await meeting_service.get_meeting(db, meeting_id)
            if meeting is None:
                await interaction.response.send_message(
                    f"Nie znaleziono spotkania #{meeting_id}.", ephemeral=True
                )
                return

            remind_at = meeting.start_time - timedelta(minutes=minutes_before)
            if user is not None:
                target_type, target_id = "user", str(user.id)
            else:
                target_type, target_id = "role", str(role.id)

            text = message or f"Przypomnienie o spotkaniu: {meeting.title}"

            try:
                reminder = await reminder_service.create_reminder(
                    db, meeting_id, target_type, target_id, remind_at, text
                )
            except ValueError as exc:
                await interaction.response.send_message(
                    f"Błąd: {exc}", ephemeral=True
                )
                return

        await interaction.response.send_message(
            f"Przypomnienie #{reminder.id} ustawione na "
            f"{remind_at.strftime(DATETIME_FORMAT)}."
        )

    @group.command(name="list", description="Lista przypomnień dla spotkania")
    @app_commands.describe(meeting_id="ID spotkania")
    async def list_reminders(
        self, interaction: discord.Interaction, meeting_id: int
    ):
        async with AsyncSessionLocal() as db:
            reminders = await reminder_service.get_reminders_for_meeting(
                db, meeting_id
            )

        if not reminders:
            await interaction.response.send_message(
                f"Brak przypomnień dla spotkania #{meeting_id}."
            )
            return

        embed = discord.Embed(
            title=f"Przypomnienia — spotkanie #{meeting_id}",
            color=discord.Color.orange(),
        )
        for r in reminders:
            status = "✅ wysłane" if r.sent else "⏳ oczekuje"
            embed.add_field(
                name=f"#{r.id} — {r.target_type} {r.target_id}",
                value=f"{r.remind_at.strftime(DATETIME_FORMAT)} — {status}",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RemindersCog(bot))
