from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards import comment_decision_keyboard
from app.states import MoodState
from app.texts import (
    comment_decision_text,
)

router = Router()


@router.message(MoodState.waiting_for_daily_answer)
async def save_daily_answer(
    message: Message,
    state: FSMContext,
) -> None:
    text = (message.text or "").strip()

    if not text:
        await message.answer("Напиши ответ на вопрос дня.")
        return

    await state.update_data(daily_answer=text)
    await state.set_state(MoodState.waiting_for_comment_decision)

    await message.answer(
        comment_decision_text(),
        reply_markup=comment_decision_keyboard(),
    )
