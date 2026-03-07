from typing import Type, List, Optional
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models import Post
from src.schemas.post import PostCreate, PostUpdate


class PostRepository:
    def __init__(self, session: Session):
        self._model: Type[Post] = Post
        self._session = session

    def get(self, post_id: int) -> Optional[Post]:
        return (self._session.query(self._model)
                .where(self._model.id == post_id)
                .scalar())

    def get_all(self) -> List[Post]:
        return self._session.query(self._model).all()

    def create(self, post_data: PostCreate, author_id: int) -> Post:
        post = self._model(
            title=post_data.title,
            text=post_data.text,
            pub_date=post_data.pub_date,
            user_id=author_id,
            location_id=post_data.location_id,
            category_id=post_data.category_id,
            is_published=post_data.is_published
        )
        self._session.add(post)
        self._session.commit()
        self._session.refresh(post)
        return post

    def update(self, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        post = self.get(post_id)
        if not post:
            return None
        
        update_data = post_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(post, key):
                setattr(post, key, value)
        
        self._session.commit()
        self._session.refresh(post)
        return post

    def delete(self, post_id: int) -> bool:
        post = self.get(post_id)
        if not post:
            return False
        
        self._session.delete(post)
        self._session.commit()
        return True
