from datetime import date

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.adapters.daily_questions_repository import DailyQuestionRepository
from app.db.engine import AsyncSessionFactory
from app.handlers.daily_questions.common import is_admin
from app.states import DailyQuestionState
from app.texts import daily_question_text_text

router = Router()


@router.message(DailyQuestionState.waiting_for_question_date)
async def save_daily_question_date(
    message: Message,
    state: FSMContext,
) -> None:
    if not is_admin(message):
        await message.answer("У вас нет доступа к этому разделу.")
        return

    raw_text = (message.text or "").strip()

    try:
        parsed_date = date.fromisoformat(raw_text)
    except ValueError:
        await message.answer(
            "Некорректная дата.\n"
            "Введите дату в формате YYYY-MM-DD.\n"
            "Например: 2026-04-22"
        )
        return

    await state.update_data(question_date=parsed_date.isoformat())
    await state.set_state(DailyQuestionState.waiting_for_question_text)
    await message.answer(daily_question_text_text())


@router.message(DailyQuestionState.waiting_for_question_text)
async def save_daily_question_text(
    message: Message,
    state: FSMContext,
) -> None:
    if not is_admin(message):
        await message.answer("У вас нет доступа к этому разделу.")
        return

    question = (message.text or "").strip()
    if not question:
        await message.answer("Вопрос не должен быть пустым. Отправьте текст вопроса.")
        return

    data = await state.get_data()
    question_date_raw = data.get("question_date")
    if not isinstance(question_date_raw, str):
        await state.clear()
        await message.answer("Состояние сбилось. Начните заново с /daily_questions")
        return

    question_date = date.fromisoformat(question_date_raw)

    async with AsyncSessionFactory() as session:
        repo = DailyQuestionRepository(session)

        old_question = await repo.get_by_date(question_date)
        saved_question = await repo.upsert_by_date(
            question_date=question_date,
            question=question,
        )

    if old_question is None:
        await message.answer(
            "Вопрос дня сохранён.\n\n"
            f"Дата: {saved_question.question_date.isoformat()}\n"
            f"Вопрос: {saved_question.question}"
        )
    else:
        await message.answer(
            "Вопрос дня обновлён.\n\n"
            f"Дата: {saved_question.question_date.isoformat()}\n"
            f"Новый вопрос: {saved_question.question}"
        )

    await state.clear()
