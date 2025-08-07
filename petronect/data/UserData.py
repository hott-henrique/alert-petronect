import typing as t

from sqlalchemy import (String, ForeignKey)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)
from sqlalchemy.dialects.postgresql import ARRAY

from petronect.base.BaseData import BaseData


class UserData(BaseData):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[t.List[str]] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)

    alerts: Mapped[list["AlertData"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

class AlertData(BaseData):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[t.List[str]] = mapped_column(String)
    words: Mapped[t.List[str]] = mapped_column(ARRAY(String))
    tokens: Mapped[t.List[str]] = mapped_column(ARRAY(String))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", use_alter=True))
    user: Mapped[UserData] = relationship(back_populates="alerts")
