from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository, PostRepository
from schemas.comment import CommentResponse
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CommentNotFoundException

class GetCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_id: int) -> CommentResponse:
        with self._database.session() as session:
            repo = CommentRepository(session)
            
            try:
                comment = repo.get(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)

            return CommentResponse.model_validate(comment)
