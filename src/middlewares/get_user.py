import random
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import TelegramObject

from config import Config
from src.repo import DB


class GetUserMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        db: DB = data['db']

        user = await db.user.get_by_tg(event.from_user.id)
        if not user:
            tasks = await db.task.all()
            random.shuffle(tasks)
            user = await db.user.create(
                tg_id=event.from_user.id,
                tg_username=event.from_user.username,
                tasks=tasks,
            )
        elif user.tg_username != event.from_user.username:
            await db.user.update(user, tg_username=event.from_user.username)

        data['user'] = user

        return await handler(event, data)
