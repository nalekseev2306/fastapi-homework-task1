from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse


class GetUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_id: int) -> UserResponse:
        with self._database.session() as session:
            repo = UserRepository(session)

            user = repo.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with id "{user_id}" not found'
                )

            return UserResponse.model_validate(user)
