from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.callbacks import (
    MoodScoreCallback,
)
from app.keyboards import (
    energy_keyboard,
)
from app.states import MoodState
from app.texts import (
    eneregy_level_text,
)

router = Router()


@router.callback_query(MoodState.waiting_for_mood, MoodScoreCallback.filter())
async def save_mood_score(
    callback: CallbackQuery,
    callback_data: MoodScoreCallback,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.update_data(
        username=callback.from_user.username or "",
        fullname=callback.from_user.full_name,
        tg_id=callback.from_user.id,
        mood_score=callback_data.score,
    )
    await state.set_state(MoodState.waiting_for_energy)

    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            f"Сегодня твое настроение: {callback_data.score}/5"
        )
        await callback.message.answer(
            eneregy_level_text(),
            parse_mode="HTML",
            reply_markup=energy_keyboard(),
        )
