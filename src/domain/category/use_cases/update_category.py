from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse, CategoryUpdate
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    CategoryWithSlugAlreadyExistException
)


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> CategoryResponse:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            try:
                category = repo.get(category_id)
            except NotFoundException:
                raise CategoryNotFoundException(id=category_id)

            if category_data.slug:
                try:
                    category_with_slug = repo.get_by_slug(category_data.slug)
                    if category_with_slug.id != category.id:
                        raise CategoryWithSlugAlreadyExistException(category_data.slug)
                except NotFoundException:
                    pass

            updated_category = repo.update(category_id, category_data)
            return CategoryResponse.model_validate(updated_category)
