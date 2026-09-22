import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from loguru import logger

from app.adapters import MoodSpreadsheet
from app.bot import create_bot, create_dispatcher
from app.core import GoogleSpreadsheet
from app.db.init_db import init_db
from app.handlers import register_handlers
from app.middlewares import ServicesMiddleware
from app.settings import settings


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    logger.info("Starting up")

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="help", description="Show help"),
            BotCommand(command="about", description="About the bot"),
            BotCommand(command="mood", description="Share your mood"),
            BotCommand(command="practices", description="Show available practices"),
        ]
    )

    await init_db()

    gs_manager = await GoogleSpreadsheet.create(
        creds_path=settings.g_creds_path,
        g_spread_key=settings.g_spread_key,
    )
    mood_ss = MoodSpreadsheet(gs_manager=gs_manager)

    dispatcher.workflow_data["gs_manager"] = gs_manager
    dispatcher.workflow_data["mood_ss"] = mood_ss

    logger.info("Startup complete")


async def on_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    logger.info("Shutting down")

    gs_manager: GoogleSpreadsheet | None = dispatcher.workflow_data.get("gs_manager")
    if gs_manager is not None:
        await gs_manager.close_spreadsheet()

    logger.info("Shutdown complete")


async def main() -> None:
    bot = create_bot()
    dp = create_dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(ServicesMiddleware())
    dp.callback_query.middleware(ServicesMiddleware())

    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
