from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_id: int) -> None:
        with self._database.session() as session:
            repo = PostRepository(session)

            post = repo.get(post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Post with id "{post_id}" not found'
                )

            success = repo.delete(post_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f'Failed to delete post with id "{post_id}"'
                )

            return None
