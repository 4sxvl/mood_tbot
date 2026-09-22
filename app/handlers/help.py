from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer("/start - start bot\n/help - show help\n/about - about bot")


@router.message(Command("about"))
async def about_handler(message: Message) -> None:
    await message.answer("This is a bot built with aiogram.")
