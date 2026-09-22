import asyncio
from collections.abc import Sequence
from pathlib import Path

import gspread
from gspread import Client, Spreadsheet, Worksheet
from loguru import logger


class WorksheetsCache:
    def __init__(self) -> None:
        self._worksheets: dict[int, Worksheet] = {}

    def add_worksheet(self, worksheet_ix: int, worksheet: Worksheet) -> Worksheet:
        if worksheet_ix in self._worksheets:
            return self._worksheets[worksheet_ix]
        self._worksheets[worksheet_ix] = worksheet
        return self._worksheets[worksheet_ix]

    def get_worksheet(self, worksheet_ix: int) -> Worksheet | None:
        return self._worksheets.get(worksheet_ix)


class GoogleSpreadsheet:
    def __init__(self, gc: Client, spread: Spreadsheet) -> None:
        self.gc = gc
        self.spread = spread
        self._worksheets: WorksheetsCache = WorksheetsCache()
        self._get_worksheet_lock: asyncio.Lock = asyncio.Lock()
        self._worksheet_append_lock: asyncio.Lock = asyncio.Lock()

    @staticmethod
    async def create(creds_path: Path, g_spread_key: str) -> GoogleSpreadsheet:
        try:
            gc = await asyncio.to_thread(gspread.service_account, filename=creds_path)
        except Exception:
            logger.exception("GoogleSpreadsheet: failed to autorize")
            raise
        try:
            spread = await asyncio.to_thread(gc.open_by_key, key=g_spread_key)
        except Exception:
            logger.exception("GoogleSpreadsheet: spreadsheets key is wrong")
            raise
        return GoogleSpreadsheet(gc=gc, spread=spread)

    async def close_spreadsheet(self) -> None:
        await asyncio.to_thread(self.spread.client.session.close)

    async def _get_worksheet(self, worksheet_ix: int) -> Worksheet:
        worksheet = self._worksheets.get_worksheet(worksheet_ix)
        if worksheet is not None:
            return worksheet
        async with self._get_worksheet_lock:
            worksheet = self._worksheets.get_worksheet(worksheet_ix)
            if worksheet is not None:
                return worksheet
            try:
                worksheet = await asyncio.to_thread(
                    self.spread.get_worksheet, index=worksheet_ix
                )
            except Exception:
                logger.exception(
                    f"GoogleSpreadsheet: no worksheet with index: {worksheet_ix}"
                )
                raise
            self._worksheets.add_worksheet(worksheet_ix, worksheet)
            return worksheet

    async def append_row(
        self, values: Sequence[str | int | float], worksheet_ix: int = 0
    ) -> None:
        worksheet = await self._get_worksheet(worksheet_ix)
        try:
            async with self._worksheet_append_lock:
                await asyncio.to_thread(worksheet.append_row, values=values)
        except Exception:
            logger.exception(f"GoogleSpreadsheet: failed to append row: {values}")
            raise
