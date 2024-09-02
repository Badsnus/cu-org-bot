from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class StartTaskCallbackData(CallbackData, prefix='task_start'):
    ...


class NextTaskCallbackData(CallbackData, prefix='task_next'):
    ...


class NextStartMessageCallbackData(CallbackData, prefix='start_next'):
    ...


start_task_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Я на месте', callback_data=StartTaskCallbackData().pack()),
    ],
])

go_to_next_start_message = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Погнали', callback_data=NextStartMessageCallbackData().pack()),
    ],
])

start_quest_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Начать квест', callback_data=NextTaskCallbackData().pack()),
    ],
])
go_to_next_task_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='ГОУ ТУ НЕКСТ ТОЧКА', callback_data=NextTaskCallbackData().pack()),
    ],
])
