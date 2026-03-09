from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from schemas.location import LocationResponse


class GetLocationBySlugUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, name: str) -> LocationResponse:
        with self._database.session() as session:
            repo = LocationRepository(session)

            location = repo.get_by_name(name)
            if not location:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Location with name "{name}" not found'
                )

            return LocationResponse.model_validate(location)
