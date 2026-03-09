from typing import List
from fastapi import APIRouter, status, Depends

from schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from domain.category.use_cases import *


router = APIRouter()


@router.get('/categories/', response_model=List[CategoryResponse],
            status_code=status.HTTP_200_OK)
async def get_all_categories(
    use_case: GetCategoriesUseCase = Depends()
) -> List[CategoryResponse]:
    return await use_case.execute()


@router.get('/categories/{category_id}', response_model=CategoryResponse,
            status_code=status.HTTP_200_OK)
async def get_category(
    category_id: int,
    use_case: GetCategoryUseCase = Depends()
) -> CategoryResponse:
    return await use_case.execute(category_id=category_id)


@router.get('/categories/by-slug/{slug}', response_model=CategoryResponse,
            status_code=status.HTTP_200_OK)
async def get_category_by_categoryname(
    slug: str,
    use_case: GetCategoryBySlugUseCase = Depends()
) -> CategoryResponse:
    return await use_case.execute(slug=slug)


@router.post('/categories/', response_model=CategoryResponse,
             status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    use_case: CreateCategoryUseCase = Depends()
) -> CategoryResponse:
    return await use_case.execute(category_data=category_data)


@router.put('/categories/{category_id}', response_model=CategoryResponse,
            status_code=status.HTTP_200_OK)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    use_case: UpdateCategoryUseCase = Depends()
) -> CategoryResponse:
    return await use_case.execute(
        category_id=category_id, category_data=category_data
    )


@router.delete('/categories/{category_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends()
) -> None:
    return await use_case.execute(category_id=category_id)
