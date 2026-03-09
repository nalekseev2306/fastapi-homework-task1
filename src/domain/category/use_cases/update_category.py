from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse, CategoryUpdate


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> CategoryResponse:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            if not repo.get(category_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Category with id "{category_id}" not found'
                )

            if category_data.slug:
                category_with_slug = repo.get_by_slug(category_data.slug)
                if category_with_slug and category_with_slug.id != category_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Category with slug "{category_data.slug}" already exists'
                    )

            updated_category = repo.update(category_id, category_data)
            return CategoryResponse.model_validate(updated_category)
