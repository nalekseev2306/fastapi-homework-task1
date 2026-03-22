from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse, UserUpdate
from core.exceptions.database_exceptions import (
    NotFoundException,
    AlreadyExistsException
)
from core.exceptions.domain_exceptions import (
    UserNotFoundException,
    UserWithUsernameAlreadyExistException,
    UserWithEmailAlreadyExistException
)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        with self._database.session() as session:
            repo = UserRepository(session)

            try:
                repo.get(user_id)
            except NotFoundException:
                raise UserNotFoundException(user_id)

            if user_data.username:
                try:
                    user_with_username = repo.get_by_username(user_data.username)
                    if user_with_username and user_with_username.id != user_id:
                        raise UserWithUsernameAlreadyExistException(user_data.username)
                except NotFoundException:
                    pass

            if user_data.email:
                try:
                    user_with_email = repo.get_by_email(user_data.email)
                    if user_with_email and user_with_email.id != user_id:
                        raise UserWithEmailAlreadyExistException(user_data.email)
                except NotFoundException:
                    pass

            updated_user = repo.update(user_id, user_data)
            return UserResponse.model_validate(updated_user)
