from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import (
    PostRepository,
    CategoryRepository,
    LocationRepository
)
from schemas.post import PostResponse, PostCreate
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException
)


class CreatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_data: PostCreate, author_id: int) -> PostResponse:
        with self._database.session() as session:
            repo = PostRepository(session)
            category_repo = CategoryRepository(session)
            location_repo = LocationRepository(session)

            try:
                category_repo.get(post_data.category_id)
            except NotFoundException:
                raise CategoryNotFoundException(id=post_data.category_id)

            try:
                location_repo.get(post_data.location_id)
            except NotFoundException:
                raise LocationNotFoundException(id=post_data.location_id)

            new_post = repo.create(post_data, author_id)
            return PostResponse.model_validate(new_post)
