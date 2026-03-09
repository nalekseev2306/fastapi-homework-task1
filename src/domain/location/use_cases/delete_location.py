from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, location_id: int) -> None:
        with self._database.session() as session:
            repo = LocationRepository(session)

            location = repo.get(location_id)
            if not location:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Location with id "{location_id}" not found'
                )

            success = repo.delete(location_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f'Failed to delete location with id "{location_id}"'
                )

            return None
