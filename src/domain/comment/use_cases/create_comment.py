from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import (
    CommentRepository,
    PostRepository
)
from schemas.comment import CommentResponse, CommentCreate
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import PostNotFoundException


class CreateCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_data: CommentCreate, author_id: int) -> CommentResponse:
        with self._database.session() as session:
            repo = CommentRepository(session)
            post_repo = PostRepository(session)

            try:
                post_repo.get(comment_data.post_id)
            except NotFoundException:
                raise PostNotFoundException(id=comment_data.post_id)

            new_comment = repo.create(comment_data, author_id)
            return CommentResponse.model_validate(new_comment)
