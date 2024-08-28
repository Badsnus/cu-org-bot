from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class StartTaskCallbackData(CallbackData, prefix='task_start'):
    ...


start_task_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Я на месте', callback_data=StartTaskCallbackData().pack()),
    ],
])

start_quest_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Начать квест', callback_data=StartTaskCallbackData().pack()),
    ],
])
