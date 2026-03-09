from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse, CategoryCreate


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, category_data: CategoryCreate) -> CategoryResponse:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            if repo.get_by_slug(category_data.slug):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Category with slug "{category_data.slug}" already exists'
                )

            new_category = repo.create(category_data)
            return CategoryResponse.model_validate(new_category)
