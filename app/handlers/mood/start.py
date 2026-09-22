from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.adapters import MoodRepository
from app.callbacks import MoodResumeCallback
from app.db.engine import AsyncSessionFactory
from app.keyboards import mood_resume_keyboard, mood_score_keyboard
from app.states import MoodState
from app.texts import mood_score_text

router = Router()


async def _start_mood_question(message: Message, state: FSMContext) -> None:
    await state.set_state(MoodState.waiting_for_mood)
    await message.answer(
        mood_score_text(),
        reply_markup=mood_score_keyboard(),
    )


@router.message(Command("mood"))
@router.message(F.text == "Заполнить дневник")
async def start_mood_flow(message: Message, state: FSMContext) -> None:
    if not message.from_user:
        await message.answer("Не удалось определить пользователя.")
        return

    async with AsyncSessionFactory() as session:
        mood_repo = MoodRepository(session)
        already_filled = await mood_repo.exists_for_user_today(message.from_user.id)

    if already_filled:
        await message.answer(
            "Ты уже сегодня заполнял(а) дневник эмоций. Хочешь заполнить ещё раз?",
            reply_markup=mood_resume_keyboard(),
        )
        return

    await _start_mood_question(message, state)


@router.callback_query(MoodResumeCallback.filter())
async def handle_mood_resume_decision(
    callback: CallbackQuery,
    callback_data: MoodResumeCallback,
    state: FSMContext,
) -> None:
    await callback.answer()

    if not isinstance(callback.message, Message):
        return

    if callback_data.action == "cancel":
        await state.clear()
        await callback.message.edit_text("Хорошо, на сегодня оставим как есть.")
        return

    await callback.message.edit_text("Хорошо, начнём заново.")
    await _start_mood_question(callback.message, state)
