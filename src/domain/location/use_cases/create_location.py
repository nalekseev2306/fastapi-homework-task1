from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from schemas.location import LocationResponse, LocationCreate
from core.exceptions.database_exceptions import AlreadyExistsException
from core.exceptions.domain_exceptions import LocationWithNameAlreadyExistException


class CreateLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, location_data: LocationCreate) -> LocationResponse:
        with self._database.session() as session:
            repo = LocationRepository(session)

            try:
                new_location = repo.create(location_data)
            except AlreadyExistsException:
                raise LocationWithNameAlreadyExistException(location_data.name)
                
            return LocationResponse.model_validate(new_location)
