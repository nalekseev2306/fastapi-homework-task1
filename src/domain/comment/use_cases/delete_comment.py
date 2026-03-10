from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_id: int) -> None:
        with self._database.session() as session:
            repo = CommentRepository(session)

            comment = repo.get(comment_id)
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Comment with id "{comment_id}" not found'
                )

            success = repo.delete(comment_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f'Failed to delete comment with id "{comment_id}"'
                )

            return None
