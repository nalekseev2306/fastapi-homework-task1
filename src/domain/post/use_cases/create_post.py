from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import (
    PostRepository, UserRepository,
    CategoryRepository, LocationRepository
)
from schemas.post import PostResponse, PostCreate
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    UserNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException
)


class CreatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_data: PostCreate) -> PostResponse:
        with self._database.session() as session:
            repo = PostRepository(session)
            user_repo = UserRepository(session)
            category_repo = CategoryRepository(session)
            location_repo = LocationRepository(session)

            try:
                user_repo.get(post_data.user_id)
            except NotFoundException:
                raise UserNotFoundException(id=post_data.user_id)

            try:
                category_repo.get(post_data.category_id)
            except NotFoundException:
                raise CategoryNotFoundException(id=post_data.category_id)

            try:
                location_repo.get(post_data.location_id)
            except NotFoundException:
                raise LocationNotFoundException(id=post_data.location_id)

            new_post = repo.create(post_data)
            return PostResponse.model_validate(new_post)
