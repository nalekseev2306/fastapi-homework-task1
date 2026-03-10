from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository
from schemas.comment import CommentResponse, CommentUpdate


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_id: int, comment_data: CommentUpdate) -> CommentResponse:
        with self._database.session() as session:
            repo = CommentRepository(session)

            if not repo.get(comment_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Comment with id "{comment_id}" not found'
                )

            updated_comment = repo.update(comment_id, comment_data)
            return CommentResponse.model_validate(updated_comment)
