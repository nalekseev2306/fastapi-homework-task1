from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .post import Post
    from .comment import Comment

class User(BaseModel):
    __tablename__ = 'users'

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
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[List['Post']] = relationship(
        'Post',
        back_populates='author'
    )
    comments: Mapped[List['Comment']] = relationship(
        'Comment',
        back_populates='author'   
    )
