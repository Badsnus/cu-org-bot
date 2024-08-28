from datetime import datetime

from sqlalchemy import BIGINT, Boolean, Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)

    photo_filename = Column(String)
    photo_file_id = Column(String)

    video_filename = Column(String)
    video_file_id = Column(String)

    address = Column(String)
    description = Column(String)
    question = Column(String)

    clue1 = Column(String)
    clue2 = Column(String)

    answers = Column(String)

    user_tasks = relationship('UserTask', back_populates='task')


class UserTask(Base):
    __tablename__ = 'users_tasks'

    user_id = Column(BIGINT, ForeignKey('users.tg_id', ondelete='CASCADE'))
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'))

    task = relationship('Task', back_populates='user_tasks')
    user = relationship('User', back_populates='user_tasks')

    id = Column(Integer, primary_key=True)

    is_done = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
