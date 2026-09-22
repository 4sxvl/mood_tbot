from datetime import datetime, time, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.models import MoodResult as MoodResultDB
from app.schemas import MoodResult


class MoodRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, mood_result: MoodResult) -> MoodResultDB:
        db_mood_result = MoodResultDB(**mood_result.model_dump())

        self.session.add(db_mood_result)
        await self.session.commit()
        await self.session.refresh(db_mood_result)

        return db_mood_result

    async def exists_for_user_today(self, tg_id: int) -> bool:
        tz = timezone(timedelta(hours=3))
        now = datetime.now(tz)

        day_start = datetime.combine(now.date(), time.min, tzinfo=tz)
        next_day_start = day_start + timedelta(days=1)

        stmt = (
            select(MoodResultDB)
            .where(MoodResultDB.tg_id == tg_id)
            .where(MoodResultDB.submitted_at >= day_start)
            .where(MoodResultDB.submitted_at < next_day_start)
            .limit(1)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
