from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import PostRepository
from schemas.user import UserResponse
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
        current_user: UserResponse
    ) -> None:
        with self._database.session() as session:
            repo = PostRepository(session)

            try:
                post = repo.get(post_id)
            except NotFoundException:
                raise PostNotFoundException(id=post_id)

            if not current_user.is_superuser and post.user_id != current_user.id:
                raise DomainPermissionDeniedException(method='delete', model='posts')

            repo.delete(post_id)
