from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            repo = CategoryRepository(session)

            category = repo.get(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Category with id "{category_id}" not found'
                )

            success = repo.delete(category_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f'Failed to delete category with id "{category_id}"'
                )

            return None
