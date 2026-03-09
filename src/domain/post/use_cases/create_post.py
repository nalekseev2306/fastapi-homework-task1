from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import PostRepository
from schemas.post import PostResponse, PostCreate


class CreatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_data: PostCreate) -> PostResponse:
        with self._database.session() as session:
            repo = PostRepository(session)

            new_post = repo.create(post_data)
            return PostResponse.model_validate(new_post)
