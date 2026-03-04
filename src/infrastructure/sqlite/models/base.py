from typing import Optional
from datetime import datetime

from infrastructure.sqlite.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
        # index=True, # pk автоматически создает index
        autoincrement=True
    )


class PublishStatusMixin:
    pub_date: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    is_published: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )
