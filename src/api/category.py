from typing import List
from fastapi import APIRouter, status, Depends

from schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from domain.category.use_cases import *
from core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    CategoryNotFoundBySlugException,
    CategoryWithSlugAlreadyExistException
)
from core.exceptions.api_exceptions import (
    NotFoundByFieldException,
    AlreadyExistWithFieldException
)


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
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundException as exc:
        raise NotFoundByFieldException(exc)

@router.get('/categories/by-slug/{slug}', response_model=CategoryResponse,
            status_code=status.HTTP_200_OK)
async def get_category_by_slug(
    slug: str,
    use_case: GetCategoryBySlugUseCase = Depends()
) -> CategoryResponse:
    try:
        return await use_case.execute(slug=slug)
    except CategoryNotFoundBySlugException as exc:
        raise NotFoundByFieldException(exc)


@router.post('/categories/', response_model=CategoryResponse,
             status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    use_case: CreateCategoryUseCase = Depends()
) -> CategoryResponse:
    try:
        return await use_case.execute(category_data=category_data)
    except CategoryWithSlugAlreadyExistException as exc:
        raise AlreadyExistWithFieldException(exc)


@router.put('/categories/{category_id}', response_model=CategoryResponse,
            status_code=status.HTTP_200_OK)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    use_case: UpdateCategoryUseCase = Depends()
) -> CategoryResponse:
    try:
        return await use_case.execute(
            category_id=category_id, category_data=category_data
        )
    except CategoryNotFoundException as exc:
        raise NotFoundByFieldException(exc)
    except CategoryWithSlugAlreadyExistException as exc:
        raise AlreadyExistWithFieldException(exc)


@router.delete('/categories/{category_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends()
) -> None:
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundException as exc:
        raise NotFoundByFieldException(exc)
