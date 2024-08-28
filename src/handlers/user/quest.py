from aiogram import Router, types

from src.keyboards.start_task import NextTaskCallbackData, start_task_keyboard
from src.repo import DB

router = Router()


@router.callback_query(NextTaskCallbackData.filter())
async def show_new_task(call: types.CallbackQuery, db: DB) -> None:
    try:
        await call.message.delete()
    except:
        pass
    task = await db.task.get_next(call.from_user.id)

    if task is None:
        await call.message.answer('Вы закончили квест')
        return

    await call.message.answer_photo(
        task.photo_file_id,
        caption=f'{task.description}\n'
                f'Твой следующий адрес: <code>{task.address}</code>',
        reply_markup=start_task_keyboard,
    )
