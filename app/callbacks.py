from aiogram.filters.callback_data import CallbackData


class MoodResumeCallback(CallbackData, prefix="mood_resume"):
    action: str


class MoodScoreCallback(CallbackData, prefix="mood"):
    score: int


class EnergyLevelCallback(CallbackData, prefix="energy"):
    level: str


class EmotionCallback(CallbackData, prefix="emotion"):
    action: str
    code: str


class MoodFactorCallback(CallbackData, prefix="mood_factor"):
    code: str


class DayChangeWishCallback(CallbackData, prefix="day_change_wish"):
    code: str


class DailyQuestionsMenuCallback(CallbackData, prefix="daily_questions"):
    action: str


class CommentDecisionCallback(CallbackData, prefix="comment"):
    action: str


class PracticeDecisionCallback(CallbackData, prefix="practice_decision"):
    action: str


class PracticeSelectCallback(CallbackData, prefix="practice_select"):
    practice_id: str


class PracticesMenuCallback(CallbackData, prefix="practices_menu"):
    action: str
