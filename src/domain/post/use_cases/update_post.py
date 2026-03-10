from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import (PostRepository, 
    CategoryRepository, LocationRepository
)
from schemas.post import PostResponse, PostUpdate


class UpdatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_id: int, post_data: PostUpdate) -> PostResponse:
        with self._database.session() as session:
            repo = PostRepository(session)
            category_repo = CategoryRepository(session)
            location_repo = LocationRepository(session)

            existing_post = repo.get(post_id)
            if not existing_post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Post with id "{post_id}" not found'
                )
            
            if post_data.category_id and post_data.category_id != existing_post.category_id:
                if not category_repo.get(post_data.category_id):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Category with id "{post_data.category_id}" not found'
                    )

            if post_data.location_id and post_data.location_id != existing_post.location_id:
                if not location_repo.get(post_data.location_id):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Location with id "{post_data.location_id}" not found'
                    )

            updated_post = repo.update(post_id, post_data)
            return PostResponse.model_validate(updated_post)
