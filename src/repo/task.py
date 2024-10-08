from typing import Sequence

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, UserTask, Task


class TaskRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def all(self) -> Sequence[Task]:
        return (await self.session.scalars(select(Task))).all()

    async def get_next(self, tg_id: int) -> Task | None:
        return await self.session.scalar(
            select(Task)
            .join(UserTask, UserTask.task_id == Task.id)
            .filter(and_(UserTask.user_id == tg_id, UserTask.is_done == False))
            .order_by(UserTask.id)
            .limit(1)
        )

    async def update(self, task: Task, **kwargs) -> Task:
        for k, v in kwargs.items():
            setattr(task, k, v)

        await self.session.commit()
        return task

    async def set_task_is_done(self, user_id: int, task_id: int) -> None:
        await self.session.execute(
            update(UserTask)
            .filter(and_(UserTask.user_id == user_id, UserTask.task_id == task_id))
            .values(is_done=True)
        )
        await self.session.commit()
