from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import UserNotFoundException


class GetUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_id: int) -> UserResponse:
        with self._database.session() as session:
            repo = UserRepository(session)

            try:
                user = repo.get(user_id)
            except NotFoundException:
                raise UserNotFoundException(id=user_id)

            return UserResponse.model_validate(user)
