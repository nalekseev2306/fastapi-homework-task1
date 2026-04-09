from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import PostRepository
from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    PostNotFoundException,
    DomainPermissionDeniedException
)


class DeletePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self,
        post_id: int,
        current_user_id: int
    ) -> None:
        with self._database.session() as session:
            repo = PostRepository(session)

            try:
                post = repo.get(post_id)
            except NotFoundException:
                raise PostNotFoundException(id=post_id)

            if post.user_id != current_user_id:
                raise DomainPermissionDeniedException(method='delete', model='posts')

            repo.delete(post_id)
