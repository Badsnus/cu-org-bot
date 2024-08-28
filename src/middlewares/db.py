from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import Config
from src.repo import DB


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker, config: Config):
        super().__init__()
        self.session_pool = session_pool
        self.config = config

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['db'] = DB(session)
            data['config'] = self.config
            return await handler(event, data)
