from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.user import UserResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    NotEnoughRightsException
)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self,
        category_id: int,
        current_user: UserResponse
    ) -> None:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            if not current_user.is_superuser:
                raise NotEnoughRightsException(current_user.username)

            try:
                repo.delete(category_id)
            except NotFoundException:
                raise CategoryNotFoundException(category_id)
