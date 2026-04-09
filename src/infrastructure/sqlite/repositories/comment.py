from typing import Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from infrastructure.sqlite.models import Comment
from schemas.comment import CommentCreate, CommentUpdate
from core.exceptions.database_exceptions import NotFoundException


class CommentRepository:
    def __init__(self, session: Session):
        self._model: Type[Comment] = Comment
        self._session = session

    def get(self, comment_id: int) -> Optional[Comment]:
        query = (
            select(self._model)
            .where(self._model.id == comment_id)
        )

        comment = self._session.scalar(query)
        if not comment:
            raise NotFoundException()

        return comment

    def get_all(self) -> List[Comment]:
        return self._session.query(self._model).all()

    def create(self, comment_data: CommentCreate, author_id: int) -> Comment:
        query = (
            insert(self._model)
            .values(**comment_data.model_dump(), user_id=author_id)
            .returning(self._model)
        )

        comment = self._session.scalar(query)
        return comment

    def update(self, comment_id: int,
               comment_data: CommentUpdate) -> Optional[Comment]:
        comment = self.get(comment_id)
        
        update_data = comment_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(comment, key):
                setattr(comment, key, value)
        
        self._session.commit()
        self._session.refresh(comment)
        return comment

    def delete(self, comment_id: int) -> bool:
        comment = self.get(comment_id)
        
        self._session.delete(comment)
        self._session.commit()
        return True
