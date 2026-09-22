from loguru import logger

from app.core import GoogleSpreadsheet
from app.keyboards import EMOTION_LABELS
from app.schemas import MoodResult


class MoodSpreadsheet:
    def __init__(self, gs_manager: GoogleSpreadsheet) -> None:
        self.gs_manager = gs_manager

    async def write_mood_result(
        self, mood_result: MoodResult, worksheet_ix: int = 0
    ) -> None:
        try:
            result_dict = mood_result.model_dump(mode="json")
            result_dict["emotions"] = ", ".join(
                EMOTION_LABELS.get(code, "unknown_code")
                for code in result_dict.get("emotions", [])
            )
            await self.gs_manager.append_row(
                values=list(result_dict.values()),
                worksheet_ix=worksheet_ix,
            )
        except Exception:
            logger.exception(
                f"MoodSpreadsheet: failed to write result for tg_id={mood_result.tg_id}: {mood_result}"
            )
