from typing import List

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    is_questioned: Mapped[bool] = mapped_column(default=False, nullable=True)
    position: Mapped[str] = mapped_column(nullable=True)
    major_id: Mapped[int] = mapped_column(ForeignKey("majors.id"), nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    second_name: Mapped[str] = mapped_column(nullable=True)
    degree: Mapped[str] = mapped_column(nullable=True)
    course: Mapped[int] = mapped_column(nullable=True)
    number: Mapped[str] = mapped_column(nullable=True)


class Major(Base):
    __tablename__ = 'majors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    user: Mapped[List["User"]] = relationship(lazy='selectin')
