from aiogram import Dispatcher

from app.handlers import daily_questions, help, mood, practices, start


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(mood.router)
    dp.include_router(daily_questions.router)
    dp.include_router(practices.router)
