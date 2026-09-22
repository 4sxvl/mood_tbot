from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.models import DailyQuestion


class DailyQuestionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_last_questions(self, limit: int = 14) -> list[DailyQuestion]:
        stmt = (
            select(DailyQuestion)
            .order_by(DailyQuestion.question_date.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_date(self, question_date: date) -> DailyQuestion | None:
        stmt = select(DailyQuestion).where(DailyQuestion.question_date == question_date)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert_by_date(
        self,
        question_date: date,
        question: str,
    ) -> DailyQuestion:
        daily_question = await self.get_by_date(question_date)

        if daily_question is None:
            daily_question = DailyQuestion(
                question_date=question_date,
                question=question,
            )
            self.session.add(daily_question)
        else:
            daily_question.question = question

        await self.session.commit()
        await self.session.refresh(daily_question)
        return daily_question
