from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import PostRepository
from schemas.post import PostResponse


class GetPostsUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[PostResponse]:
        with self._database.session() as session:
            repo = PostRepository(session)

            posts = repo.get_all()

            return [PostResponse.model_validate(post) for post in posts]
