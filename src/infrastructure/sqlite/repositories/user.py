from typing import Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert

from infrastructure.sqlite.models import User
from schemas.user import UserCreate, UserUpdate
from core.exceptions.database_exceptions import (
    NotFoundException,
    AlreadyExistsException
)


class UserRepository:
    def __init__(self, session: Session):
        self._model: Type[User] = User
        self._session = session

    def get(self, user_id: int) -> Optional[User]:
        query = (
            select(self._model)
            .where(self._model.id == user_id)
        )

        user = self._session.scalar(query)
        if not user:
            raise NotFoundException()
        
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        query = (
            select(self._model)
            .where(self._model.username == username)
        )

        user = self._session.scalar(query)
        if not user:
            raise NotFoundException()
        
        return user
    
    def get_by_email(self, email: str) -> Optional[User]:
        query = (
            select(self._model)
            .where(self._model.email == email)
        )

        user = self._session.scalar(query)
        if not user:
            raise NotFoundException()
        
        return user

    def get_all(self) -> List[User]:
        return self._session.query(self._model).all()

    def create(self, user_data: UserCreate) -> User:
        data = user_data.model_dump()
        
        query = (
            insert(self._model)
            .values(data)
            .returning(self._model)
        )

        try:
            user = self._session.scalar(query)
        except IntegrityError:
            raise AlreadyExistsException()

        return user

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get(user_id)

        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self._session.commit()
        self._session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get(user_id)
        
        self._session.delete(user)
        self._session.commit()
        return True
