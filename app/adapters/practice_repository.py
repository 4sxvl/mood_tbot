import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.models import Practice


class PracticeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Practice]:
        stmt = select(Practice).order_by(Practice.title)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, practice_id: str) -> Practice | None:
        try:
            practice_uuid = uuid.UUID(practice_id)
        except ValueError:
            return None

        stmt = select(Practice).where(Practice.id == practice_uuid)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
