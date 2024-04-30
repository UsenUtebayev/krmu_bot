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
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_types.id"), nullable=True)
    major_id: Mapped[int] = mapped_column(ForeignKey("majors.id"), nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)


class UserType(Base):
    __tablename__ = 'user_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    user: Mapped[List["User"]] = relationship(lazy='selectin')


class Major(Base):
    __tablename__ = 'majors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    user: Mapped[List["User"]] = relationship(lazy='selectin')
