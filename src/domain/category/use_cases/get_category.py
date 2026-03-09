from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse


class GetCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, category_id: int) -> CategoryResponse:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            category = repo.get(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Category with id "{category_id}" not found'
                )

            return CategoryResponse.model_validate(category)
