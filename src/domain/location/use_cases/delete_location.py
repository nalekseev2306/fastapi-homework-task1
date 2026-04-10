from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from schemas.user import UserResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    LocationNotFoundException,
    NotEnoughRightsException
)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self,
        location_id: int,
        current_user: UserResponse
    ) -> None:
        with self._database.session() as session:
            repo = LocationRepository(session)

            if not current_user.is_superuser:
                raise NotEnoughRightsException(current_user.username)

            try:
                repo.delete(location_id)
            except NotFoundException:
                raise LocationNotFoundException(id=location_id)
