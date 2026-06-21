import asyncio
import logging

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


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        logger.info("Zsynchronizowano %d komend slash", len(synced))
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
