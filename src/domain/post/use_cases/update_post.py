from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import (PostRepository, 
    CategoryRepository, LocationRepository
)
from schemas.post import PostResponse, PostUpdate
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    DomainPermissionDeniedException
)

class UpdatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self,
        post_id: int,
        post_data: PostUpdate,
        current_user_id: int
    ) -> PostResponse:
        with self._database.session() as session:
            repo = PostRepository(session)
            category_repo = CategoryRepository(session)
            location_repo = LocationRepository(session)

            try:
                existing_post = repo.get(post_id)
            except NotFoundException:
                raise PostNotFoundException(id=post_id)
            
            if existing_post.id != current_user_id:
                raise DomainPermissionDeniedException(method='update', model='posts')

            if post_data.category_id and post_data.category_id != existing_post.category_id:
                try:
                    category_repo.get(post_data.category_id)
                except NotFoundException:
                    raise CategoryNotFoundException(id=post_data.category_id)

            if post_data.location_id and post_data.location_id != existing_post.location_id:
                try:
                    location_repo.get(post_data.location_id)
                except NotFoundException:
                    raise LocationNotFoundException(id=post_data.location_id)

            updated_post = repo.update(post_id, post_data)
            return PostResponse.model_validate(updated_post)
