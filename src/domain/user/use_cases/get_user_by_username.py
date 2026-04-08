import logging

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByUsernameException

logger = logging.getLogger(__name__)


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database

    async def execute(
            self,
            username: str,
            current_user: UserResponse | None = None
    ) -> UserResponse:
        with self._database.session() as session:
            repo = UserRepository(session)

            try:
                user = repo.get_by_username(username)
            except NotFoundException:
                error = UserNotFoundByUsernameException(username=username)
                logger.error(f'User {current_user.usernmae} make error: {error.get_detail()}')
                raise error

            return UserResponse.model_validate(user)
