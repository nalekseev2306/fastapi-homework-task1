from typing import Type, List, Optional
from sqlalchemy.orm import Session

from infrastructure.sqlite.models import Comment
from schemas.comment import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self, session: Session):
        self._model: Type[Comment] = Comment
        self._session = session

    def get(self, comment_id: int) -> Optional[Comment]:
        return (self._session.query(self._model)
                .where(self._model.id == comment_id)
                .scalar())

    def get_all(self) -> List[Comment]:
        return self._session.query(self._model).all()

    def create(self, comment_data: CommentCreate,
               author_id: int) -> Comment:
        comment = self._model(
            text=comment_data.text,
            post_id=comment_data.post_id,
            user_id=author_id
        )
        self._session.add(comment)
        self._session.commit()
        self._session.refresh(comment)
        return comment

    def update(self, comment_id: int,
               comment_data: CommentUpdate) -> Optional[Comment]:
        comment = self.get(comment_id)
        if not comment:
            return None
        
        update_data = comment_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(comment, key):
                setattr(comment, key, value)
        
        self._session.commit()
        self._session.refresh(comment)
        return comment

    def delete(self, comment_id: int) -> bool:
        comment = self.get(comment_id)
        if not comment:
            return False
        
        self._session.delete(comment)
        self._session.commit()
        return True
