from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    UserNotFoundException,
    DomainPermissionDeniedException
)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self,
        user_id: int,
        current_user_id: int
    ) -> None:
        with self._database.session() as session:
            repo = UserRepository(session)

            try:
                repo.get(user_id)
            except NotFoundException:
                raise UserNotFoundException(id=user_id)
            
            if user_id != current_user_id:
                raise DomainPermissionDeniedException(method='delete', model='user')

            repo.delete(user_id)
