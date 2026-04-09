from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CommentNotFoundException,
    DomainPermissionDeniedException
)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self,
        comment_id: int,
        current_user_id: int
    ) -> None:
        with self._database.session() as session:
            repo = CommentRepository(session)

            try:
                comment = repo.get(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)

            if comment.user_id != current_user_id:
                raise DomainPermissionDeniedException(method='delete', model='comments')

            repo.delete(comment_id)
