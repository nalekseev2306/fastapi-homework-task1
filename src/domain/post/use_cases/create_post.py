from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import (PostRepository, 
    UserRepository, CategoryRepository, LocationRepository
)
from schemas.post import PostResponse, PostCreate


class CreatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_data: PostCreate) -> PostResponse:
        with self._database.session() as session:
            repo = PostRepository(session)
            user_repo = UserRepository(session)
            category_repo = CategoryRepository(session)
            location_repo = LocationRepository(session)

            if not user_repo.get(post_data.user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Author with id "{post_data.user_id}" not found'
                )

            if not category_repo.get(post_data.category_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Category with id "{post_data.category_id}" not found'
                )

            if not location_repo.get(post_data.location_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Location with id "{post_data.location_id}" not found'
                )

            new_post = repo.create(post_data)
            return PostResponse.model_validate(new_post)
