from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.adapters.daily_questions_repository import DailyQuestionRepository
from app.callbacks import DailyQuestionsMenuCallback
from app.db.engine import AsyncSessionFactory
from app.handlers.daily_questions.common import is_admin
from app.states import DailyQuestionState
from app.texts import (
    daily_question_cancelled_text,
    daily_question_date_text,
)

router = Router()


@router.callback_query(DailyQuestionsMenuCallback.filter(F.action == "list"))
async def list_daily_questions(
    callback: CallbackQuery,
) -> None:
    if not is_admin(callback):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.answer()

    async with AsyncSessionFactory() as session:
        repo = DailyQuestionRepository(session)
        questions = await repo.get_last_questions(limit=14)

    if not isinstance(callback.message, Message):
        return

    if not questions:
        await callback.message.answer("Вопросов дня пока нет.")
        return

    lines = ["Последние 14 вопросов дня:\n"]
    for item in questions:
        lines.append(f"{item.question_date.isoformat()} — {item.question}")

    await callback.message.answer("\n".join(lines))


@router.callback_query(DailyQuestionsMenuCallback.filter(F.action == "upsert"))
async def start_upsert_daily_question(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not is_admin(callback):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.answer()
    await state.clear()
    await state.set_state(DailyQuestionState.waiting_for_question_date)

    if isinstance(callback.message, Message):
        await callback.message.answer(daily_question_date_text())


@router.callback_query(DailyQuestionsMenuCallback.filter(F.action == "cancel"))
async def cancel_daily_questions(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not is_admin(callback):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.answer()
    await state.clear()

    if isinstance(callback.message, Message):
        await callback.message.answer(daily_question_cancelled_text())
