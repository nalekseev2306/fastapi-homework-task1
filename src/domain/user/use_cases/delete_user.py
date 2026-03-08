from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_id: int) -> None:
        with self._database.session() as session:
            repo = UserRepository(session)

            user = repo.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with id "{user_id}" not found'
                )

            success = repo.delete(user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f'Failed to delete user with id "{user_id}"'
                )

            # return {"message": f'User with id "{user_id}" was deleted'}
            return None
