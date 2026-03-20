from typing import Type, List, Optional
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from infrastructure.sqlite.models import Category
from schemas.category import CategoryCreate, CategoryUpdate
from core.exceptions.database_exceptions import (
    NotFoundException,
    AlreadyExistsException
)


class CategoryRepository:
    def __init__(self, session: Session):
        self._model: Type[Category] = Category
        self._session = session

    def get(self, category_id: int) -> Optional[Category]:
        query = (
            select(self._model)
            .where(self._model.id == category_id)
        )

        user = self._session.scalar(query)
        if not user:
            raise NotFoundException()

        return user

    def get_by_slug(self, slug: str) -> Optional[Category]:
        query = (
            select(self._model)
            .where(self._model.slug == slug)
        )

        user = self._session.scalar(query)
        if not user:
            raise NotFoundException()

        return user

    def get_all(self) -> List[Category]:
        return self._session.query(self._model).all()

    def create(self, category_data: CategoryCreate) -> Category:
        query = (
            insert(self._model)
            .values(category_data.model_dump())
            .returning(self._model)
        )
        
        try:
            category = self._session.scalar(query)
        except IntegrityError:
            raise AlreadyExistsException()
        
        return category

    def update(self, category_id: int, 
               category_data: CategoryUpdate) -> Optional[Category]:
        category = self.get(category_id)
        
        update_data = category_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(category, key):
                setattr(category, key, value)
        
        self._session.commit()
        self._session.refresh(category)
        return category

    def delete(self, category_id: int) -> bool:
        category = self.get(category_id)

        self._session.delete(category)
        self._session.commit()
        return True
