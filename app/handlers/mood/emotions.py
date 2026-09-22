from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.callbacks import (
    EmotionCallback,
)
from app.keyboards import (
    emotions_keyboard,
    mood_factor_keyboard,
)
from app.states import MoodState
from app.texts import (
    mood_factor_text,
)

router = Router()


@router.callback_query(
    MoodState.waiting_for_emotions,
    EmotionCallback.filter(F.action == "toggle"),
)
async def toggle_emotion(
    callback: CallbackQuery,
    callback_data: EmotionCallback,
    state: FSMContext,
) -> None:
    await callback.answer()

    data = await state.get_data()
    selected: list[str] = data.get("emotions", [])
    code = callback_data.code

    if code in selected:
        selected = [item for item in selected if item != code]
    else:
        selected = [*selected, code]

    await state.update_data(emotions=selected)

    if isinstance(callback.message, Message):
        await callback.message.edit_reply_markup(
            reply_markup=emotions_keyboard(selected),
        )


@router.callback_query(
    MoodState.waiting_for_emotions,
    EmotionCallback.filter(F.action == "done"),
)
async def finish_emotions(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    selected: list[str] = data.get("emotions", [])

    if not selected:
        await callback.answer("Выбери хотя бы одну эмоцию", show_alert=True)
        return

    await callback.answer()
    await state.set_state(MoodState.waiting_for_main_factor)

    if isinstance(callback.message, Message):
        await callback.message.edit_text("Эмоции сохранены.")
        await callback.message.answer(
            mood_factor_text(),
            parse_mode="HTML",
            reply_markup=mood_factor_keyboard(),
        )
