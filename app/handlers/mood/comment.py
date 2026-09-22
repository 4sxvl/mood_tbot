from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.adapters import MoodSpreadsheet
from app.callbacks import (
    CommentDecisionCallback,
)
from app.handlers.mood.practices import go_to_practices_or_finish
from app.states import MoodState

router = Router()


@router.callback_query(
    MoodState.waiting_for_comment_decision,
    CommentDecisionCallback.filter(),
)
async def save_comment_decision(
    callback: CallbackQuery,
    callback_data: CommentDecisionCallback,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    action = callback_data.action

    if action == "yes":
        await callback.answer()
        await state.set_state(MoodState.waiting_for_comment_text)

        if isinstance(callback.message, Message):
            await callback.message.edit_text("Напиши комментарий.")
        return

    await state.update_data(comment="")
    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.edit_text("Комментарий пропущен.")
        await go_to_practices_or_finish(
            message=callback.message,
            state=state,
            mood_ss=mood_ss,
        )


@router.message(MoodState.waiting_for_comment_text)
async def save_comment_text(
    message: Message,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    text = (message.text or "").strip()

    if not text:
        await message.answer("Напиши комментарий или вернись назад.")
        return

    await state.update_data(comment=text)

    await go_to_practices_or_finish(
        message=message,
        state=state,
        mood_ss=mood_ss,
    )
