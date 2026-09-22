from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Dispatcher


class ServicesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        dispatcher: Dispatcher = data["dispatcher"]

        data["mood_ss"] = dispatcher.workflow_data["mood_ss"]
        data["gs_manager"] = dispatcher.workflow_data["gs_manager"]

        return await handler(event, data)
