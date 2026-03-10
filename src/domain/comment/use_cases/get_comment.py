from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository, PostRepository
from schemas.comment import CommentResponse


class GetCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_id: int) -> CommentResponse:
        with self._database.session() as session:
            repo = CommentRepository(session)

            comment = repo.get(comment_id)
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Comment with id "{comment_id}" not found'
                )

            return CommentResponse.model_validate(comment)
