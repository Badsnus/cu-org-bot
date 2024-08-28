from aiogram import Router, types
from aiogram.filters import CommandStart

from src.models import User
from src.repo import DB

router = Router()


@router.message(CommandStart())
async def start(message: types.Message, user: User, db: DB) -> None:
    ...
