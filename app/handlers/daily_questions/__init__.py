from aiogram import Router

from app.handlers.daily_questions import actions, menu, upsert

router = Router()

router.include_router(menu.router)
router.include_router(actions.router)
router.include_router(upsert.router)
