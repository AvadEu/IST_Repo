import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.session import AsyncSessionLocal
from services import reminder_service

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def check_reminders(bot):
    """Pobiera oczekujące przypomnienia i wysyła je jako wiadomości prywatne."""
    async with AsyncSessionLocal() as db:
        pending = await reminder_service.get_pending_reminders(db)

        for reminder in pending:
            try:
                if reminder.target_type == "user":
                    user = bot.get_user(int(reminder.target_id))
                    if user is None:
                        user = await bot.fetch_user(int(reminder.target_id))
                    if user is not None:
                        await user.send(reminder.message)

                elif reminder.target_type == "role":
                    for guild in bot.guilds:
                        role = guild.get_role(int(reminder.target_id))
                        if role is None:
                            continue
                        for member in role.members:
                            await member.send(reminder.message)

                await reminder_service.mark_sent(db, reminder.id)
            except Exception:  # noqa: BLE001 — nie przerywaj pętli z powodu jednego DM
                logger.exception("Nie udało się wysłać przypomnienia %s", reminder.id)


def setup_scheduler(bot):
    scheduler.add_job(check_reminders, "interval", seconds=60, args=[bot])
    return scheduler
