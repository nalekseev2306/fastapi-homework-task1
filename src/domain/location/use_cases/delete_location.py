from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import LocationRepository
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import LocationNotFoundException


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, location_id: int) -> None:
        with self._database.session() as session:
            repo = LocationRepository(session)

            try:
                repo.delete(location_id)
            except NotFoundException:
                raise LocationNotFoundException(id=location_id)
