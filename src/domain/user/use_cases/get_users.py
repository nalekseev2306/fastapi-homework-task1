from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import UserRepository
from schemas.user import UserResponse


class GetUsersUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[UserResponse]:
        with self._database.session() as session:
            repo = UserRepository(session)

            users = repo.get_all()

            return [UserResponse.model_validate(user) for user in users]
