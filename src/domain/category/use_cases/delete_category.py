from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CategoryNotFoundException


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            try:
                repo.delete(category_id)
            except NotFoundException:
                raise CategoryNotFoundException(category_id)
