from sqlalchemy import BIGINT, Column, String

from .base import Base


class User(Base):
    __tablename__ = 'users'

    tg_id = Column(BIGINT, primary_key=True, autoincrement=False)
    tg_username = Column(String, nullable=True)
