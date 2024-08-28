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


async def send_go_to_next_task_message(message: types.Message, text: str) -> None:
    await message.answer(
        text,
        reply_markup=go_to_next_task_keyboard,
    )


@router.callback_query(NextTaskCallbackData.filter())
async def show_new_task(call: types.CallbackQuery, db: DB) -> None:
    try:
        await call.message.delete()
    except:
        pass
    task = await db.task.get_next(call.from_user.id)

    if task is None:
        await call.message.answer(get_quest_end_text())
        return

    await call.message.answer_photo(
        photo=task.photo_file_id,
        caption=f'{task.description}\n'
                f'Твой следующий адрес: <code>{task.address}</code>',
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
        caption=f'А вот и вопрос, на который тебе нужно ответить: {task.question}\n\n'
                f'Пиши ответ ниже 👇',
    )

    await state.set_state(QuestionState.answer)


@router.message(QuestionState.answer)
async def validate_answer(message: types.Message, db: DB, state: FSMContext) -> None:
    task = await db.task.get_next(message.from_user.id)

    if task is None:
        await message.answer(get_quest_end_text())
        await state.clear()
        return

    answer = message.text
    answers = task.answers.split(';')
    if answer in answers:
        await db.task.set_task_is_done(task_id=task.id, user_id=message.from_user.id)
        await state.clear()
        await send_go_to_next_task_message(message,
                                           'Поздравляю - это правильный ответ!\n'
                                           'Быстрее переходи к следующему заданию')
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
        f'Увы, ты не смог правильно ответить - правильный ответ был: {answers[0]}\n'
        f'<b>Но не расстраивайся - дальше тебя ждет еще больше крутых локаций!</b>',
    )
