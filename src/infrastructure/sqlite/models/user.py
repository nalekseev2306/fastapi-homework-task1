from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        unique=True,
        # index используется для быстрого поиска в бд по данному полю
        index=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        nullable=False
    )
