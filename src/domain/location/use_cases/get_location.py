from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from schemas.location import LocationResponse


class GetLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, location_id: int) -> LocationResponse:
        with self._database.session() as session:
            repo = LocationRepository(session)

            location = repo.get(location_id)
            if not location:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Location with id "{location_id}" not found'
                )

            return LocationResponse.model_validate(location)
