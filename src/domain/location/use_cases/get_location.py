from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from schemas.location import LocationResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import LocationNotFoundException


class GetLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, location_id: int) -> LocationResponse:
        with self._database.session() as session:
            repo = LocationRepository(session)

            try:
                location = repo.get(location_id)
            except NotFoundException:
                raise LocationNotFoundException(location_id)

            return LocationResponse.model_validate(location)
