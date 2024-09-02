from aiogram import Router, types
from aiogram.filters import CommandStart

from src.keyboards.start_task import (
    go_to_next_start_message,
    start_quest_keyboard,
    NextStartMessageCallbackData,

)

router = Router()


# @router.message()
# async def gg(message: types.Message):
#     print(message.video.file_id)


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(
        """
<b>Приветствуем тебя, студент Центрального университета, на курсе Основы Российской Государственности.</b>

Мы бы хотели помочь тебе познакомиться с историческим и культурным разнообразием городского пространства, показать, сколько историй и смыслов оно скрывает. 
А еще это хорошая возможность познакомиться с преподавательской группой нашего курса до начала учебы. Каждый преподаватель выбрал близ станции метро «Маяковская» одну локацию, о которой он расскажет тебе свою историю. 
Надеемся, наш квест поможет тебе понять и открыть те места, мимо которых ты будешь ходить и видеть ближайшие годы. 
        """,
        reply_markup=go_to_next_start_message,
    )


@router.callback_query(NextStartMessageCallbackData.filter())
async def start_quest(call: types.CallbackQuery):
    await call.message.edit_text(
        """
Точки будут предлагаться тебе в случайном порядке. После того, как закончится приветствие, ты получишь адрес первой локации. На месте посмотри видео с небольшим рассказом от преподавателя, внимательно осмотри локацию, а затем разгадай предложенную загадку. В случае неправильного ответа, бот отправит тебе подсказку. Всего их 2. После прохождения одной локации, бот отправит тебе новую. Всего будет 9 мест. 

<b>Желаем хорошо провести время. Удачи на заданиях!</b>
        """,
        reply_markup=start_quest_keyboard,
    )
