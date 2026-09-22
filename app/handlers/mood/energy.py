from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.callbacks import (
    EnergyLevelCallback,
)
from app.keyboards import (
    emotions_keyboard,
)
from app.states import MoodState

router = Router()

ENERGY_LEVELS = {"high": "Высокая", "medium": "Средняя", "low": "Низкая"}


@router.callback_query(MoodState.waiting_for_energy, EnergyLevelCallback.filter())
async def save_energy(
    callback: CallbackQuery,
    callback_data: EnergyLevelCallback,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.update_data(
        energy_level=callback_data.level,
        emotions=[],
    )
    await state.set_state(MoodState.waiting_for_emotions)

    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            f"Сегодня твоя энергия: {ENERGY_LEVELS[callback_data.level]}"
        )
        await callback.message.answer(
            "Какие эмоции ты испытал(а) сегодня?\nМожно выбрать несколько вариантов.",
            reply_markup=emotions_keyboard(),
        )
