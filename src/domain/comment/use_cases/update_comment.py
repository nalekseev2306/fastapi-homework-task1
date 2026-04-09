from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository
from schemas.comment import CommentResponse, CommentUpdate
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CommentNotFoundException,
    DomainPermissionDeniedException
)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self,
        comment_id: int,
        comment_data: CommentUpdate,
        current_user_id: int
    ) -> CommentResponse:
        with self._database.session() as session:
            repo = CommentRepository(session)

            try:
                comment = repo.get(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)
            
            if comment.user_id != current_user_id:
                raise DomainPermissionDeniedException(method='update', model='comments')

            updated_comment = repo.update(comment_id, comment_data)
            return CommentResponse.model_validate(updated_comment)
