import asyncio

from aiogram import Bot, types


async def do_backup(bot: Bot, config) -> None:
    while True:
        await asyncio.sleep(86400 // 24)
        await bot.send_document(
            chat_id=config.backup_channel_id,
            document=types.FSInputFile('main.db'),
        )
