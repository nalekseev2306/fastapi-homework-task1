from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse, CategoryCreate
from core.exceptions.database_exceptions import AlreadyExistsException
from core.exceptions.domain_exceptions import CategoryWithSlugAlreadyExistException


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, category_data: CategoryCreate) -> CategoryResponse:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            try:
                new_category = repo.create(category_data)
            except AlreadyExistsException:
                raise CategoryWithSlugAlreadyExistException(category_data.slug)

            return CategoryResponse.model_validate(new_category)
