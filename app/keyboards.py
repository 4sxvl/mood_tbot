from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.callbacks import (
    CommentDecisionCallback,
    DailyQuestionsMenuCallback,
    DayChangeWishCallback,
    EmotionCallback,
    EnergyLevelCallback,
    MoodFactorCallback,
    MoodResumeCallback,
    MoodScoreCallback,
    PracticeDecisionCallback,
    PracticeSelectCallback,
    PracticesMenuCallback,
)
from app.db.models import Practice

EMOTION_LABELS: dict[str, str] = {
    "inspiration": "Воодушевление",
    "joy": "Радость",
    "calm": "Спокойствие / умиротворение",
    "sadness": "Тоска / грусть",
    "anxiety": "Тревога / раздражение",
    "fatigue": "Усталость",
    "indifference": "Равнодушие",
    "hurt": "Обида",
    "shame": "Стыд",
    "guilt": "Вина",
    "disappointment": "Разочарование",
    "anger": "Злость",
}


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="Заполнить дневник")
    builder.button(text="Список практик")

    builder.adjust(2)
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выбери действие",
    )


def mood_resume_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Продолжить",
        callback_data=MoodResumeCallback(action="continue"),
    )
    builder.button(
        text="Отмена",
        callback_data=MoodResumeCallback(action="cancel"),
    )

    builder.adjust(1)
    return builder.as_markup()


def mood_score_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    moods = {
        "очень хорошее": 5,
        "скорее хорошее": 4,
        "нормальное": 3,
        "скорее плохоe": 2,
        "очень плохое": 1,
    }
    for score in moods:
        builder.button(
            text=str(score),
            callback_data=MoodScoreCallback(score=moods[score]),
        )

    builder.adjust(1)
    return builder.as_markup()


def energy_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Высокая",
        callback_data=EnergyLevelCallback(level="high"),
    )
    builder.button(
        text="Средняя",
        callback_data=EnergyLevelCallback(level="medium"),
    )
    builder.button(
        text="Низкая",
        callback_data=EnergyLevelCallback(level="low"),
    )

    builder.adjust(1)
    return builder.as_markup()


def emotions_keyboard(selected: list[str] | None = None) -> InlineKeyboardMarkup:
    selected_set = set(selected or [])
    builder = InlineKeyboardBuilder()

    for code, label in EMOTION_LABELS.items():
        prefix = "✓ " if code in selected_set else ""
        builder.button(
            text=f"{prefix}{label}",
            callback_data=EmotionCallback(action="toggle", code=code),
        )

    builder.button(
        text="Записать ответ",
        callback_data=EmotionCallback(action="done", code="done"),
    )

    builder.adjust(1)
    return builder.as_markup()


MOOD_FACTOR_LABELS: dict[str, str] = {
    "social": "Общение с другими людьми",
    "work": "Учёба или работа",
    "inner": "Моё внутреннее состояние",
    "physical": "Физическое самочувствие",
    "event": "Какое-то конкретное событие",
    "other": "Другое",
}


def mood_factor_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for code, label in MOOD_FACTOR_LABELS.items():
        builder.button(
            text=label,
            callback_data=MoodFactorCallback(code=code),
        )

    builder.adjust(1)
    return builder.as_markup()


DAY_CHANGE_WISH_LABELS: dict[str, str] = {
    "alot": "Да, многое",
    "alittle": "Да, немногое",
    "allgood": "Нет, все устраивало",
    "noidea": "Затрудняюсь ответить",
    "other": "Другое",
}


def day_change_wish_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for code, label in DAY_CHANGE_WISH_LABELS.items():
        builder.button(
            text=label,
            callback_data=DayChangeWishCallback(code=code),
        )

    builder.adjust(1)
    return builder.as_markup()


def comment_decision_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да",
        callback_data=CommentDecisionCallback(action="yes"),
    )
    builder.button(
        text="Нет",
        callback_data=CommentDecisionCallback(action="no"),
    )

    builder.adjust(1)
    return builder.as_markup()


def daily_questions_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Показать последние 14",
        callback_data=DailyQuestionsMenuCallback(action="list"),
    )
    builder.button(
        text="Добавить / изменить вопрос",
        callback_data=DailyQuestionsMenuCallback(action="upsert"),
    )
    builder.button(
        text="Отмена",
        callback_data=DailyQuestionsMenuCallback(action="cancel"),
    )

    builder.adjust(1)
    return builder.as_markup()


def practice_offer_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да",
        callback_data=PracticeDecisionCallback(action="yes"),
    )
    builder.button(
        text="Нет",
        callback_data=PracticeDecisionCallback(action="no"),
    )

    builder.adjust(1)
    return builder.as_markup()


def practices_keyboard(practices: list[Practice]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for practice in practices:
        builder.button(
            text=practice.title,
            callback_data=PracticeSelectCallback(practice_id=str(practice.id)),
        )

    builder.adjust(1)
    return builder.as_markup()


def practices_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад к списку",
        callback_data=PracticesMenuCallback(action="back"),
    )
    return builder.as_markup()
