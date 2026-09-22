from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field


class MoodResult(BaseModel):
    tg_id: int | None = None
    username: str | None = None
    fullname: str | None = None
    mood_score: int | None = None
    energy_level: str | None = None
    emotions: list | None = None
    mood_factor: str | None = None
    day_change_wish: str | None = None
    daily_question: str | None = None
    daily_answer: str | None = None
    comment: str | None = None
    selected_practice: str | None = None
    submitted_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone(timedelta(hours=3)))
    )
