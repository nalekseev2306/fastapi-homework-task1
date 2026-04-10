from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository
from schemas.user import UserResponse
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
        current_user: UserResponse
    ) -> None:
        with self._database.session() as session:
            repo = CommentRepository(session)

            try:
                comment = repo.get(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)

            if not current_user.is_superuser and comment.user_id != current_user.id:
                raise DomainPermissionDeniedException(method='delete', model='comments')

            repo.delete(comment_id)
