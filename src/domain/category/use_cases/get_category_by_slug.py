from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, slug: str) -> CategoryResponse:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            category = repo.get_by_slug(slug)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Category with slug "{slug}" not found'
                )

            return CategoryResponse.model_validate(category)
