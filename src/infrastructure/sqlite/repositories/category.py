from typing import Type, List, Optional
from sqlalchemy.orm import Session

from infrastructure.sqlite.models import Category
from schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: Session):
        self._model: Type[Category] = Category
        self._session = session

    def get(self, category_id: int) -> Optional[Category]:
        return (self._session.query(self._model)
                .where(self._model.id == category_id)
                .scalar())

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return (self._session.query(self._model)
                .where(self._model.slug == slug)
                .scalar())

    def get_all(self) -> List[Category]:
        return self._session.query(self._model).all()

    def create(self, category_data: CategoryCreate) -> Category:
        category = self._model(
            name=category_data.name,
            description=category_data.description,
            slug=category_data.slug
        )
        self._session.add(category)
        self._session.commit()
        self._session.refresh(category)
        return category

    def update(self, category_id: int, 
               category_data: CategoryUpdate) -> Optional[Category]:
        category = self.get(category_id)
        if not category:
            return None
        
        update_data = category_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(category, key):
                setattr(category, key, value)
        
        self._session.commit()
        self._session.refresh(category)
        return category

    def delete(self, category_id: int) -> bool:
        category = self.get(category_id)
        if not category:
            return False

        self._session.delete(category)
        self._session.commit()
        return True
