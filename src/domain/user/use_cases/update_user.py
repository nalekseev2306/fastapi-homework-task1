from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse, UserUpdate


class UpdateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        with self._database.session() as session:
            repo = UserRepository(session)

            if not repo.get(user_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with id "{user_id}" not found'
                )

            if user_data.username:
                user_with_username = repo.get_by_username(user_data.username)
                if user_with_username and user_with_username.id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'User with username "{user_data.username}" already exists'
                    )

            if user_data.email:
                user_with_email = repo.get_by_email(user_data.email)
                if user_with_email and user_with_email.id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'User with email "{user_data.email}" already exists'
                    )

            updated_user = repo.update(user_id, user_data)
            return UserResponse.model_validate(updated_user)
