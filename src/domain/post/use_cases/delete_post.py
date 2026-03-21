from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import PostRepository
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import PostNotFoundException


class DeletePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_id: int) -> None:
        with self._database.session() as session:
            repo = PostRepository(session)

            try:
                repo.delete(post_id)
            except NotFoundException:
                raise PostNotFoundException(id=post_id)

            return None
