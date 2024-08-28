import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config, load_config
from src.handlers import routers
from src.middlewares import DbSessionMiddleware, GetUserMiddleware
from src.models import Base
from src.services import do_backup

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info('Starting bot')

    config: Config = load_config()

    engine = create_async_engine(url=config.db_connection, echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    # TODO миграций нет - мб стоит их добавить
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot: Bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode='HTML'),
    )
    dp: Dispatcher = Dispatcher()

    x = await bot.send_photo(config.backup_channel_id, types.FSInputFile('media/tasks.jpg'))
    config.tasks_photo_file_id = x.photo[-1].file_id

    dp.include_routers(*routers)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker, config=config))
    dp.message.outer_middleware(GetUserMiddleware())
    dp.callback_query.outer_middleware(GetUserMiddleware())

    asyncio.create_task(do_backup(bot, config))

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
