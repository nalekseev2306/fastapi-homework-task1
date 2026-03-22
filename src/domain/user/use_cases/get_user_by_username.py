from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByUsernameException


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, username: int) -> UserResponse:
        with self._database.session() as session:
            repo = UserRepository(session)

            try:
                user = repo.get_by_username(username)
            except NotFoundException:
                raise UserNotFoundByUsernameException(username=username)

            return UserResponse.model_validate(user)
