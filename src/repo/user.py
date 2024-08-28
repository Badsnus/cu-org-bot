from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


class UserRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def all(self) -> Sequence[User]:
        return (await self.session.scalars(select(User).filter(User.fio != 'FIO'))).all()

    async def get_by_tg(self, tg_id: int) -> User | None:
        return await self.session.scalar(select(User).filter(User.tg_id == tg_id))

    async def create(self, telegram_id: int, tg_username: str | None) -> User:
        user = User(
            tg_id=telegram_id,
            tg_username=tg_username,
        )

        self.session.add(user)

        await self.session.commit()
        return user

    async def update(self, user: User, **kwargs) -> User:
        for k, v in kwargs.items():
            setattr(user, k, v)

        await self.session.commit()
        return user
