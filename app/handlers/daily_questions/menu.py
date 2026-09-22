from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.handlers.daily_questions.common import is_admin
from app.keyboards import daily_questions_menu_keyboard
from app.texts import daily_questions_menu_text

router = Router()


@router.message(Command("daily_questions"))
async def daily_questions_menu(message: Message, state: FSMContext) -> None:
    if not is_admin(message):
        await message.answer("У вас нет доступа к этому разделу.")
        return

    await state.clear()
    await message.answer(
        daily_questions_menu_text(),
        reply_markup=daily_questions_menu_keyboard(),
    )
