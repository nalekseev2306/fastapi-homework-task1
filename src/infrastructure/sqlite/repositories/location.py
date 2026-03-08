from typing import Type, List, Optional
from sqlalchemy.orm import Session

from infrastructure.sqlite.models import Location
from schemas.location import LocationCreate


class LocationRepository:
    def __init__(self, session: Session):
        self._model: Type[Location] = Location
        self._session = session

    def get(self, location_id: int) -> Optional[Location]:
        return (self._session.query(self._model)
                .where(self._model.id == location_id)
                .scalar())

    def get_by_name(self, name: str) -> Optional[Location]:
        return (self._session.query(self._model)
                .where(self._model.name == name)
                .scalar())

    def get_all(self) -> List[Location]:
        return self._session.query(self._model).all()

    def create(self, location_data: LocationCreate) -> Location:
        location = self._model(
            name=location_data.name
        )
        self._session.add(location)
        self._session.commit()
        self._session.refresh(location)
        return location

    def delete(self, location_id: int) -> bool:
        location = self.get(location_id)
        if not location:
            return False
        
        self._session.delete(location)
        self._session.commit()
        return True
