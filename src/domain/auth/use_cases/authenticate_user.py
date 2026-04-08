from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse
from resources.auth import verify_password
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    InvalidPasswordException
)


class AuthenticateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self,
        username: str,
        password: str
    ) -> UserResponse:
        with self._database.session() as session:
            try:
                repo = UserRepository(session)
                user = repo.get_by_username(username=username)
            except NotFoundException:
                raise UserNotFoundByUsernameException(username)
            
            if not verify_password(plain_password=password, hashed_password=user.password):
                    raise InvalidPasswordException
                
            return UserResponse.model_validate(obj=user)

