from typing import Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from infrastructure.sqlite.models import Post
from schemas.post import PostCreate, PostUpdate
from core.exceptions.database_exceptions import NotFoundException


class PostRepository:
    def __init__(self, session: Session):
        self._model: Type[Post] = Post
        self._session = session

    def get(self, post_id: int) -> Optional[Post]:
        query = (
            select(self._model)
            .where(self._model.id == post_id)
        )

        post = self._session.scalar(query)
        if not post:
            raise NotFoundException()

        return post

    def get_all(self) -> List[Post]:
        return self._session.query(self._model).all()

    def create(self, post_data: PostCreate) -> Post:
        query = (
            insert(self._model)
            .values(post_data.model_dump())
            .returning(self._model)
        )

        post = self._session.scalar(query)
        return post

    def update(self, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        post = self.get(post_id)
        
        update_data = post_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(post, key):
                setattr(post, key, value)
        
        self._session.commit()
        self._session.refresh(post)
        return post

    def delete(self, post_id: int) -> bool:
        post = self.get(post_id)
        
        self._session.delete(post)
        self._session.commit()
        return True
