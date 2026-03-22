from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByEmailException


class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, email: int) -> UserResponse:
        with self._database.session() as session:
            repo = UserRepository(session)

            try:
                user = repo.get_by_email(email)
            except NotFoundException:
                raise UserNotFoundByEmailException(email=email)
            
            return UserResponse.model_validate(user)
