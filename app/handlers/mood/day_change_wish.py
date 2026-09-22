from datetime import date

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.adapters import DailyQuestionRepository
from app.callbacks import (
    DayChangeWishCallback,
)
from app.db.engine import AsyncSessionFactory
from app.keyboards import DAY_CHANGE_WISH_LABELS, comment_decision_keyboard
from app.states import MoodState
from app.texts import (
    comment_decision_text,
    day_change_wish_other_text,
    no_daily_question_text,
)

router = Router()


@router.callback_query(
    MoodState.waiting_for_day_change_wish,
    DayChangeWishCallback.filter(),
)
async def save_day_change_wish(
    callback: CallbackQuery,
    callback_data: DayChangeWishCallback,
    state: FSMContext,
) -> None:
    code = callback_data.code

    if code == "other":
        await callback.answer()
        await state.set_state(MoodState.waiting_for_day_change_wish_comment)

        if isinstance(callback.message, Message):
            await callback.message.edit_text("Ты выбрал(а): Другое.")
            await callback.message.answer(day_change_wish_other_text())
        return

    day_change_wish_text_value = DAY_CHANGE_WISH_LABELS[code]
    await state.update_data(day_change_wish=day_change_wish_text_value)

    async with AsyncSessionFactory() as session:
        daily_question_repo = DailyQuestionRepository(session)
        daily_question = await daily_question_repo.get_by_date(date.today())

    await callback.answer()

    if daily_question is not None:
        await state.update_data(daily_question=daily_question.question)
        await state.set_state(MoodState.waiting_for_daily_answer)

        if isinstance(callback.message, Message):
            await callback.message.edit_text(
                f"Желание изменить день сохранено: {day_change_wish_text_value}"
            )
            await callback.message.answer(f"Вопрос дня:\n\n{daily_question.question}")
    else:
        await state.update_data(daily_question="", daily_answer="")
        await state.set_state(MoodState.waiting_for_comment_decision)

        if isinstance(callback.message, Message):
            await callback.message.edit_text(
                f"Желание изменить день сохранено: {day_change_wish_text_value}"
            )
            await callback.message.answer(no_daily_question_text())
            await callback.message.answer(
                comment_decision_text(),
                reply_markup=comment_decision_keyboard(),
            )


@router.message(MoodState.waiting_for_day_change_wish_comment)
async def save_day_change_wish_comment(
    message: Message,
    state: FSMContext,
) -> None:
    text = (message.text or "").strip()

    if not text:
        await message.answer("Напиши коротко, что хотелось бы изменить в своём дне.")
        return

    await state.update_data(day_change_wish=text)

    async with AsyncSessionFactory() as session:
        daily_question_repo = DailyQuestionRepository(session)
        daily_question = await daily_question_repo.get_by_date(date.today())

    if daily_question is not None:
        await state.update_data(daily_question=daily_question.question)
        await state.set_state(MoodState.waiting_for_daily_answer)

        await message.answer(f"Вопрос дня:\n\n{daily_question.question}")
    else:
        await state.update_data(daily_question="", daily_answer="")
        await state.set_state(MoodState.waiting_for_comment_decision)

        await message.answer(no_daily_question_text())
        await message.answer(
            comment_decision_text(),
            reply_markup=comment_decision_keyboard(),
        )
