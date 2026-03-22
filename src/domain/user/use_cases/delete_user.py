from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import UserNotFoundException


class DeleteUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_id: int) -> None:
        with self._database.session() as session:
            repo = UserRepository(session)

            try:
                repo.delete(user_id)
            except NotFoundException:
                raise UserNotFoundException(id=user_id)
            
            return None
