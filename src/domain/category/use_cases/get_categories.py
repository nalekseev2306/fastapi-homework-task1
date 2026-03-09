from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse


class GetCategoriesUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[CategoryResponse]:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            categorys = repo.get_all()

            return [CategoryResponse.model_validate(category) for category in categorys]
