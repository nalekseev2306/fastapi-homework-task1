from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from schemas.location import LocationResponse


class GetLocationsUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[LocationResponse]:
        with self._database.session() as session:
            repo = LocationRepository(session)

            locations = repo.get_all()

            return [LocationResponse.model_validate(location) for location in locations]
