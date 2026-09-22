from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.adapters import MoodRepository, MoodSpreadsheet, PracticeRepository
from app.callbacks import (
    PracticeDecisionCallback,
    PracticeSelectCallback,
)
from app.db.engine import AsyncSessionFactory
from app.keyboards import practice_offer_keyboard, practices_keyboard
from app.schemas import MoodResult
from app.states import MoodState
from app.texts import (
    goodbye_text,
    goodbye_with_practice_text,
    practice_offer_text,
    practices_list_text,
)

router = Router()


async def finalize_mood_result(
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> MoodResult:
    data = await state.get_data()
    mood_result = MoodResult(**data)

    async with AsyncSessionFactory() as session:
        mood_repo = MoodRepository(session)
        await mood_repo.save(mood_result)

    await mood_ss.write_mood_result(mood_result)

    await state.clear()
    return mood_result


async def go_to_practices_or_finish(
    message: Message,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    data = await state.get_data()
    mood_score = data.get("mood_score")

    if isinstance(mood_score, int) and mood_score <= 3:
        await state.set_state(MoodState.waiting_for_practice_decision)
        await message.answer(
            practice_offer_text(),
            reply_markup=practice_offer_keyboard(),
        )
        return

    await state.update_data(selected_practice="")
    await finalize_mood_result(state=state, mood_ss=mood_ss)
    await message.answer(goodbye_text())


@router.callback_query(
    MoodState.waiting_for_practice_decision,
    PracticeDecisionCallback.filter(),
)
async def save_practice_decision(
    callback: CallbackQuery,
    callback_data: PracticeDecisionCallback,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    await callback.answer()

    if not isinstance(callback.message, Message):
        return

    if callback_data.action == "no":
        await state.update_data(selected_practice="")
        await finalize_mood_result(state=state, mood_ss=mood_ss)
        await callback.message.edit_text(goodbye_text())
        return

    async with AsyncSessionFactory() as session:
        practice_repo = PracticeRepository(session)
        practices = await practice_repo.get_all()

    if not practices:
        await state.update_data(selected_practice="")
        await finalize_mood_result(state=state, mood_ss=mood_ss)
        await callback.message.edit_text(
            "Сейчас у меня нет доступных практик.\n\n" + goodbye_text()
        )
        return

    await state.set_state(MoodState.waiting_for_practice_choice)
    await callback.message.edit_text(
        practices_list_text(),
        reply_markup=practices_keyboard(practices),
    )


@router.callback_query(
    MoodState.waiting_for_practice_choice,
    PracticeSelectCallback.filter(),
)
async def save_practice_choice(
    callback: CallbackQuery,
    callback_data: PracticeSelectCallback,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    await callback.answer()

    if not isinstance(callback.message, Message):
        return

    async with AsyncSessionFactory() as session:
        practice_repo = PracticeRepository(session)
        practice = await practice_repo.get_by_id(callback_data.practice_id)

    if practice is None:
        await callback.message.answer(
            "Не удалось найти эту практику. Попробуй выбрать другую."
        )
        return

    await state.update_data(selected_practice=practice.title)
    await finalize_mood_result(state=state, mood_ss=mood_ss)

    await callback.message.edit_text(f"{practice.title}\n\n{practice.description}")
    await callback.message.answer(goodbye_with_practice_text())
