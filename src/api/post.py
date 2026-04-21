from typing import List
from fastapi import APIRouter, status, Depends

from core.logging import get_logger
from schemas.post import PostResponse, PostCreate, PostUpdate
from schemas.user import UserResponse
from domain.post.use_cases import *
from core.exceptions.domain_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    DomainPermissionDeniedException
)
from core.exceptions.api_exceptions import (
    NotFoundByFieldException,
    PermissionDeniedException
)
from services.auth import AuthService


router = APIRouter()
logger = get_logger(__name__)


@router.get('/posts/', response_model=List[PostResponse],
            status_code=status.HTTP_200_OK)
async def get_all_posts(
    use_case: GetPostsUseCase = Depends()
) -> List[PostResponse]:
    return await use_case.execute()


@router.get('/posts/{post_id}', response_model=PostResponse,
            status_code=status.HTTP_200_OK)
async def get_post(
    post_id: int,
    use_case: GetPostUseCase = Depends()
) -> PostResponse:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundException as exc:
        raise NotFoundByFieldException(exc)


@router.post('/posts/', response_model=PostResponse,
             status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: CreatePostUseCase = Depends()
) -> PostResponse:
    try:
        return await use_case.execute(post_data=post_data, author_id=user.id)
    except (CategoryNotFoundException,
            LocationNotFoundException) as exc:
        logger.error(f'{exc.get_status_code()} - {user.username} failed to create post: {exc.get_detail()}')
        raise NotFoundByFieldException(exc)


@router.put('/posts/{post_id}', response_model=PostResponse,
            status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: UpdatePostUseCase = Depends()
) -> PostResponse:
    try:
        return await use_case.execute(
            post_id=post_id,
            post_data=post_data,
            current_user=user
        )
    except DomainPermissionDeniedException as exc:
        logger.error(f'{exc.get_status_code()} - {user.username}: {exc.get_detail()}')
        raise PermissionDeniedException(exc)
    except (CategoryNotFoundException,
            LocationNotFoundException) as exc:
        logger.error(f'{exc.get_status_code()} - {user.username} failed to update post: {exc.get_detail()}')
        raise NotFoundByFieldException(exc)


@router.delete('/posts/{post_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: DeletePostUseCase = Depends()
) -> None:
    try:
        return await use_case.execute(
            post_id=post_id,
            current_user=user
        )
    except DomainPermissionDeniedException as exc:
        logger.error(f'{exc.get_status_code()} - {user.username}: {exc.get_detail()}')
        raise PermissionDeniedException(exc)
    except PostNotFoundException as exc:
        logger.error(f'{exc.get_status_code()} - {user.username} failed to delete post: {exc.get_detail()}')
        raise NotFoundByFieldException(exc)
