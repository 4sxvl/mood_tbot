from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.callbacks import (
    MoodFactorCallback,
)
from app.keyboards import (
    MOOD_FACTOR_LABELS,
    day_change_wish_keyboard,
)
from app.states import MoodState
from app.texts import (
    day_change_wish_text,
    mood_factor_other_text,
)

router = Router()


@router.callback_query(
    MoodState.waiting_for_main_factor,
    MoodFactorCallback.filter(),
)
async def save_main_factor(
    callback: CallbackQuery,
    callback_data: MoodFactorCallback,
    state: FSMContext,
) -> None:
    code = callback_data.code

    if code == "other":
        await callback.answer()
        await state.set_state(MoodState.waiting_for_main_factor_comment)

        if isinstance(callback.message, Message):
            await callback.message.edit_text("Ты выбрал(а): Другое.")
            await callback.message.answer(mood_factor_other_text())
        return

    factor_text = MOOD_FACTOR_LABELS[code]

    await state.update_data(mood_factor=factor_text)
    await state.set_state(MoodState.waiting_for_day_change_wish)
    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.edit_text(f"Фактор сохранён: {factor_text}")
        await callback.message.answer(
            day_change_wish_text(),
            reply_markup=day_change_wish_keyboard(),
        )


@router.message(MoodState.waiting_for_main_factor_comment)
async def save_main_factor_comment(
    message: Message,
    state: FSMContext,
) -> None:
    text = (message.text or "").strip()

    if not text:
        await message.answer("Напиши коротко, что именно повлияло на настроение.")
        return

    await state.update_data(mood_factor=text)
    await state.set_state(MoodState.waiting_for_day_change_wish)

    await message.answer(
        day_change_wish_text(),
        reply_markup=day_change_wish_keyboard(),
    )
