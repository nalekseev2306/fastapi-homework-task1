from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import PostRepository
from schemas.post import PostResponse, PostUpdate


class UpdatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_id: int, post_data: PostUpdate) -> PostResponse:
        with self._database.session() as session:
            repo = PostRepository(session)

            if not repo.get(post_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Post with id "{post_id}" not found'
                )

            updated_post = repo.update(post_id, post_data)
            return PostResponse.model_validate(updated_post)
