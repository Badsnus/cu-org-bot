from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig
    db_connection: str
    backup_channel_id: int


def load_config() -> Config:
    load_dotenv()

    return Config(
        tg_bot=TelegramBotConfig(token=getenv('BOT_TOKEN')),
        db_connection=getenv('db_connection'),
        backup_channel_id=int(getenv('BACKUP_CHANNEL_ID')),
    )
