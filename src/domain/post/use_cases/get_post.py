from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import PostRepository
from schemas.post import PostResponse


class GetPostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_id: int) -> PostResponse:
        with self._database.session() as session:
            repo = PostRepository(session)

            post = repo.get(post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Post with id "{post_id}" not found'
                )

            return PostResponse.model_validate(post)
