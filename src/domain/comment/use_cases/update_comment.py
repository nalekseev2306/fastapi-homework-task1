from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository
from schemas.comment import CommentResponse, CommentUpdate
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CommentNotFoundException


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_id: int, comment_data: CommentUpdate) -> CommentResponse:
        with self._database.session() as session:
            repo = CommentRepository(session)

            try:
                repo.get(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)

            updated_comment = repo.update(comment_id, comment_data)
            return CommentResponse.model_validate(updated_comment)
