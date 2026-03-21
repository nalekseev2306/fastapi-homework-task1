from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository
from schemas.category import CategoryResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CategoryNotFoundBySlugException


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, slug: str) -> CategoryResponse:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            try:
                category = repo.get_by_slug(slug)
            except NotFoundException:
                raise CategoryNotFoundBySlugException(slug=slug)

            return CategoryResponse.model_validate(category)
