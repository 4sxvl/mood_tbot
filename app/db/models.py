import uuid
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
from sqlmodel import Field, SQLModel


class MoodResult(SQLModel, table=True):
    __tablename__ = "mood_results"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tg_id: int = Field(index=True)
    username: str = Field(default="")
    fullname: str
    mood_score: int
    energy_level: str
    emotions: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False),
    )
    mood_factor: str
    day_change_wish: str
    daily_question: str = Field(default="")
    daily_answer: str = Field(default="")
    comment: str = Field(default="")
    selected_practice: str = Field(default="")
    submitted_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone(timedelta(hours=3)))
    )


class DailyQuestion(SQLModel, table=True):
    __tablename__ = "daily_questions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    question: str
    question_date: date = Field(index=True, unique=True)
    submitted_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone(timedelta(hours=3)))
    )


class Practice(SQLModel, table=True):
    __tablename__ = "practices"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True, unique=True)
    description: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone(timedelta(hours=3)))
    )
