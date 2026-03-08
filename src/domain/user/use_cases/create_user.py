from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse, UserCreate


class CreateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_data: UserCreate) -> UserResponse:
        with self._database.session() as session:
            repo = UserRepository(session)

            if repo.get_by_username(user_data.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'User with username "{user_data.email}" already exists'
                )

            if repo.get_by_email(user_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'User with email "{user_data.email}" already exists'
                )

            new_user = repo.create(user_data)
            return UserResponse.model_validate(new_user)
