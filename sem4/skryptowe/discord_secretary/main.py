import asyncio
import logging

import discord
import uvicorn

from bot.client import bot
from bot.cogs.meetings_cog import MeetingsCog
from bot.cogs.reminders_cog import RemindersCog
from bot.cogs.recording_cog import RecordingCog
from bot.scheduler import scheduler, check_reminders
from config import settings
from db.session import Base, engine
from web.app import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: discord.app_commands.AppCommandError
):
    """Globalna sieć bezpieczeństwa — żadna komenda nie kończy się cichą awarią."""
    logger.exception("Błąd komendy aplikacji", exc_info=error)
    msg = "❌ Wystąpił błąd podczas obsługi komendy. Spróbuj ponownie."
    try:
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
    except discord.HTTPException:
        # interakcja już potwierdzona lub wygasła — nie ma jak odpowiedzieć
        logger.warning("Nie udało się dostarczyć komunikatu o błędzie komendy")


@bot.event
async def on_ready():
    # on_ready potrafi odpalić się wielokrotnie (każdy reconnect) — synchronizuj
    # komendy tylko raz, inaczej copy_global_to rzuci CommandAlreadyRegistered
    if getattr(bot, "_commands_synced", False):
        logger.info("Bot ponownie połączony jako %s", bot.user)
        return
    try:
        guild_id = settings.discord_guild_id
        if guild_id and guild_id.isdigit() and int(guild_id) > 0:
            # Rejestracja per-serwer propaguje się NATYCHMIAST (globalna do ~1h),
            # dzięki czemu po zmianie parametrów komend nie pojawia się
            # "komenda nieaktualna".
            guild = discord.Object(id=int(guild_id))
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            logger.info(
                "Zsynchronizowano %d komend do serwera %s", len(synced), guild_id
            )
            # usuń ewentualne stare globalne rejestracje, by nie dublowały komend
            bot.tree.clear_commands(guild=None)
            await bot.tree.sync()
        else:
            synced = await bot.tree.sync()
            logger.info("Zsynchronizowano %d komend globalnie", len(synced))
        bot._commands_synced = True
    except Exception:
        logger.exception("Nie udało się zsynchronizować komend slash")
    logger.info("Bot zalogowany jako %s", bot.user)


async def main():
    # utwórz tabele jeśli nie istnieją (fallback obok Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # załaduj cogi bota
    await bot.add_cog(MeetingsCog(bot))
    await bot.add_cog(RemindersCog(bot))
    await bot.add_cog(RecordingCog(bot))

    # uruchom scheduler sprawdzający przypomnienia co minutę
    scheduler.add_job(check_reminders, "interval", seconds=60, args=[bot])
    scheduler.start()

    # uruchom bota i serwer webowy równolegle w jednym procesie
    web_config = uvicorn.Config(
        app, host=settings.web_host, port=settings.web_port, log_level="info"
    )
    web_server = uvicorn.Server(web_config)

    await asyncio.gather(
        bot.start(settings.discord_token),
        web_server.serve(),
    )


if __name__ == "__main__":
    asyncio.run(main())
