from sqlalchemy.ext.asyncio import AsyncSession

from .task import TaskRepo
from .user import UserRepo


class DB:

    def __init__(self, session: AsyncSession):
        self.user = UserRepo(session)
        self.task = TaskRepo(session)
