from typing import Type, List, Optional
from sqlalchemy.orm import Session

from infrastructure.sqlite.models import User
from schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: Session):
        self._model: Type[User] = User
        self._session = session

    def get(self, user_id: int) -> Optional[User]:
        return (self._session.query(self._model)
                .where(self._model.id == user_id)
                .scalar())

    def get_by_username(self, username: str) -> Optional[User]:
        return (self._session.query(self._model)
                .where(self._model.username == username)
                .scalar())
    
    def get_by_email(self, email: str) -> Optional[User]:
        return (self._session.query(self._model)
                .where(self._model.email == email)
                .scalar())

    def get_all(self) -> List[User]:
        return self._session.query(self._model).all()

    def create(self, user_data: UserCreate) -> User:
        user = self._model(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password.get_secret_value(),
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(user, key):
                if key == 'password':
                    setattr(user, key, value.get_secret_value())
                else:
                    setattr(user, key, value)
        
        self._session.commit()
        self._session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get(user_id)
        if not user:
            return False
        
        self._session.delete(user)
        self._session.commit()
        return True
