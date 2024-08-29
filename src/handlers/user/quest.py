from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.keyboards.start_task import (
    go_to_next_task_keyboard,
    NextTaskCallbackData,
    StartTaskCallbackData,
    start_task_keyboard,
)
from src.repo import DB
from src.states.question import QuestionState

router = Router()


def get_quest_end_text():
    return 'Вы закончили квест'


async def send_go_to_next_task_message(message: types.Message, text: str, photo: str) -> None:
    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=go_to_next_task_keyboard,
    )


@router.callback_query(NextTaskCallbackData.filter())
async def show_new_task(call: types.CallbackQuery, db: DB) -> None:
    await call.message.edit_reply_markup()

    task = await db.task.get_next(call.from_user.id)

    if task is None:
        await call.message.answer(get_quest_end_text())
        return

    await call.message.answer_photo(
        photo=task.photo_file_id,
        caption=f'<b>Твой следующий адрес:</b>\n<code>{task.address}</code>',
        reply_markup=start_task_keyboard,
    )


@router.callback_query(StartTaskCallbackData.filter())
async def start_task(call: types.CallbackQuery, db: DB, state: FSMContext) -> None:
    task = await db.task.get_next(call.from_user.id)

    if task is None:
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer(get_quest_end_text())
        return

    await state.update_data(
        attempt=1,
    )
    await call.message.edit_reply_markup()
    await call.message.answer_video(
        video=task.video_file_id,
        caption=f'{task.question}\n\n'
                f'<b>Пиши свой ответ 👇</b>',
    )

    await state.set_state(QuestionState.answer)


@router.message(QuestionState.answer)
async def validate_answer(message: types.Message, db: DB, state: FSMContext) -> None:
    task = await db.task.get_next(message.from_user.id)

    if task is None:
        await message.answer(get_quest_end_text())
        await state.clear()
        return

    answer = message.text.lower()
    answers = task.answers.split(';')
    if answer in answers:
        await db.task.set_task_is_done(task_id=task.id, user_id=message.from_user.id)
        await state.clear()
        await send_go_to_next_task_message(
            message,
            'Поздравляю - это правильный ответ!\n\n'
            f'<b>Ответ: {answers[0]}</b>\n'
            f'{task.description}',
            task.answer_photo_file_id,
        )
        return

    data = await state.get_data()
    attempt = data.get('attempt', 1)

    if attempt < 3:
        clues = [task.clue1, task.clue2]
        await message.answer(
            f'Увы, это неправильный ответ(((\nВот тебе подсказка: <code>{clues[attempt - 1]}</code>\n\nПиши ответ ниже 👇'
        )
        await state.update_data(attempt=attempt + 1)
        return

    await db.task.set_task_is_done(task_id=task.id, user_id=message.from_user.id)
    await state.clear()
    await send_go_to_next_task_message(
        message,
        f'У тебя почти получилось!\n\n'
        f'<b>Ответ: {answers[0]}</b>\n'
        f'{task.description}',
        task.answer_photo_file_id,
    )
