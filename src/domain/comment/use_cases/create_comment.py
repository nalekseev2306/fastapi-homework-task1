from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import (CommentRepository,
    UserRepository, PostRepository
)
from schemas.comment import CommentResponse, CommentCreate
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    PostNotFoundException,
    UserNotFoundException
)


class CreateCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_data: CommentCreate) -> CommentResponse:
        with self._database.session() as session:
            repo = CommentRepository(session)
            user_repo = UserRepository(session)
            post_repo = PostRepository(session)

            try:
                user_repo.get(comment_data.user_id)
            except NotFoundException:
                raise UserNotFoundException(id=comment_data.user_id)

            try:
                post_repo.get(comment_data.post_id)
            except NotFoundException:
                raise PostNotFoundException(id=comment_data.post_id)

            new_comment = repo.create(comment_data)
            return CommentResponse.model_validate(new_comment)
