from aiogram.types import TelegramObject, User

from app.settings import settings


def extract_user(event: TelegramObject) -> User | None:
    user = getattr(event, "from_user", None)
    return user if isinstance(user, User) else None


def is_admin(event: TelegramObject) -> bool:
    user = extract_user(event)
    return user is not None and user.id in settings.admin_tg_ids
