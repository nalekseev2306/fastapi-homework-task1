from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CommentRepository
from schemas.comment import CommentResponse


class GetCommentsUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[CommentResponse]:
        with self._database.session() as session:
            repo = CommentRepository(session)

            comments = repo.get_all()

            return [CommentResponse.model_validate(comment) for comment in comments]
