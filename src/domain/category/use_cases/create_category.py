from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse, CategoryCreate
from schemas.user import UserResponse
from core.exceptions.database_exceptions import AlreadyExistsException
from core.exceptions.domain_exceptions import (
    CategoryWithSlugAlreadyExistException,
    NotEnoughRightsException
)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self,
        category_data: CategoryCreate,
        current_user: UserResponse
    ) -> CategoryResponse:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            if not current_user.is_superuser:
                raise NotEnoughRightsException(current_user.username)

            try:
                new_category = repo.create(category_data)
            except AlreadyExistsException:
                raise CategoryWithSlugAlreadyExistException(category_data.slug)

            return CategoryResponse.model_validate(new_category)
