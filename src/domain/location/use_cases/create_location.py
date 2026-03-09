from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from schemas.location import LocationResponse, LocationCreate


class CreateLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, location_data: LocationCreate) -> LocationResponse:
        with self._database.session() as session:
            repo = LocationRepository(session)

            if repo.get_by_name(location_data.name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Location with name "{location_data.name}" already exists'
                )

            new_location = repo.create(location_data)
            return LocationResponse.model_validate(new_location)
