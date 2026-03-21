from typing import Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from infrastructure.sqlite.models import Location
from schemas.location import LocationCreate
from core.exceptions.database_exceptions import (
    NotFoundException,
    AlreadyExistsException
)

class LocationRepository:
    def __init__(self, session: Session):
        self._model: Type[Location] = Location
        self._session = session

    def get(self, location_id: int) -> Optional[Location]:
        query = (
            select(self._model)
            .where(self._model.id == location_id)     
        )

        location = self._session.scalar(query)
        if not location:
            raise NotFoundException()

        return location

    def get_by_name(self, name: str) -> Optional[Location]:
        query = (
            select(self._model)
            .where(self._model.name == name)     
        )

        location = self._session.scalar(query)
        if not location:
            raise NotFoundException()

        return location

    def get_all(self) -> List[Location]:
        return self._session.query(self._model).all()

    def create(self, location_data: LocationCreate) -> Location:
        query = (
            insert(self._model)
            .values(location_data.model_dump())
            .returning(self._model)
        )
        
        try:
            location = self._session.scalar(query)
        except IntegrityError:
            raise AlreadyExistsException()
        
        return location

    def delete(self, location_id: int) -> bool:
        location = self.get(location_id)
        
        self._session.delete(location)
        self._session.commit()
        return True
