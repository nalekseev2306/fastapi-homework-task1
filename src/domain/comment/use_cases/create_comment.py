from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import (CommentRepository,
    UserRepository, PostRepository
)
from schemas.comment import CommentResponse, CommentCreate


class CreateCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_data: CommentCreate) -> CommentResponse:
        with self._database.session() as session:
            repo = CommentRepository(session)
            user_repo = UserRepository(session)
            post_repo = PostRepository(session)

            if not user_repo.get(comment_data.user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Author with id "{comment_data.user_id}" not found'
                )

            if not post_repo.get(comment_data.post_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Post with id "{comment_data.post_id}" not found'
                )

            new_comment = repo.create(comment_data)
            return CommentResponse.model_validate(new_comment)
