from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from schemas.location import LocationResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import LocationNotFoundByNameException


class GetLocationBySlugUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, name: str) -> LocationResponse:
        with self._database.session() as session:
            repo = LocationRepository(session)

            try:
                location = repo.get_by_name(name)
            except:
                raise LocationNotFoundByNameException(name=name)

            return LocationResponse.model_validate(location)
