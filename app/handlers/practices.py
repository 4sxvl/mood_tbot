from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.adapters import PracticeRepository
from app.callbacks import PracticeSelectCallback, PracticesMenuCallback
from app.db.engine import AsyncSessionFactory
from app.keyboards import practices_back_keyboard, practices_keyboard
from app.texts import no_practices_text, practices_menu_text

router = Router()


async def _load_practices():
    async with AsyncSessionFactory() as session:
        practice_repo = PracticeRepository(session)
        return await practice_repo.get_all()


@router.message(Command("practices"))
@router.message(F.text == "Список практик")
async def show_practices_menu(message: Message) -> None:
    practices = await _load_practices()

    if not practices:
        await message.answer(no_practices_text())
        return

    await message.answer(
        practices_menu_text(),
        reply_markup=practices_keyboard(practices),
    )


@router.callback_query(PracticeSelectCallback.filter())
async def show_practice_description(
    callback: CallbackQuery,
    callback_data: PracticeSelectCallback,
) -> None:
    await callback.answer()

    if not isinstance(callback.message, Message):
        return

    async with AsyncSessionFactory() as session:
        practice_repo = PracticeRepository(session)
        practice = await practice_repo.get_by_id(callback_data.practice_id)

    if practice is None:
        await callback.message.answer("Не удалось найти эту практику.")
        return

    await callback.message.edit_text(
        f"{practice.title}\n\n{practice.description}",
        reply_markup=practices_back_keyboard(),
    )


@router.callback_query(PracticesMenuCallback.filter())
async def handle_practices_menu_action(
    callback: CallbackQuery,
    callback_data: PracticesMenuCallback,
) -> None:
    await callback.answer()

    if not isinstance(callback.message, Message):
        return

    if callback_data.action != "back":
        return

    practices = await _load_practices()

    if not practices:
        await callback.message.edit_text(no_practices_text())
        return

    await callback.message.edit_text(
        practices_menu_text(),
        reply_markup=practices_keyboard(practices),
    )
