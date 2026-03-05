from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey

from .base import BaseModel
from .user import User
from .post import Post


class Comment(BaseModel):
    __tablename__ = 'comments'
    
    text: Mapped[str] = mapped_column(nullable=False) 
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )

    author: Mapped['User'] = relationship(
        'User',
        back_populates='comments'
    )
    post: Mapped[Post] = relationship(
        'Post',
        back_populates='comments'
    )
