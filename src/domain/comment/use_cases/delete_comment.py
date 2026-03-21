from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CommentNotFoundException


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_id: int) -> None:
        with self._database.session() as session:
            repo = CommentRepository(session)

            try:
                repo.delete(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)
