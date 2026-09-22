from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from app.keyboards import main_menu_keyboard
from app.texts import start_text

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    if not message.from_user:
        logger.error("No from_user")
        return
    await message.answer(
        start_text(first_name=message.from_user.first_name),
        reply_markup=main_menu_keyboard(),
    )
