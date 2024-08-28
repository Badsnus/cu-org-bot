from aiogram import Router, types
from aiogram.filters import CommandStart

from src.keyboards.start_task import start_quest_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(
        'Это мега супер сверх челледж - скорее нажимай на кнопку и начинай',
        reply_markup=start_quest_keyboard,
    )
