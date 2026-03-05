from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import BaseModel, PublishStatusMixin
from .user import User

if TYPE_CHECKING:
    from .category import Category
    from .location import Location
    from .comment import Comment


class Post(BaseModel, PublishStatusMixin):
    __tablename__ = 'posts'
    
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    pub_date: Mapped[datetime] = mapped_column(nullable=False)
    # image: Mapped[str]

    comments: Mapped[List['Comment']] = relationship(
        'Comment',
        back_populates='post'
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey('locations.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    author: Mapped['User'] = relationship(
        'User',
        back_populates='posts'
    )
    location: Mapped['Location'] = relationship(
        'Location',
        back_populates='posts'
    )
    category: Mapped['Category'] = relationship(
        'Category',
        back_populates='posts'
    )
