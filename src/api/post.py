from typing import List
from fastapi import APIRouter, status, Depends, HTTPException

from schemas.post import PostResponse, PostCreate, PostUpdate
from domain.post.use_cases import *
from core.exceptions.domain_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException
)


router = APIRouter()


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )

@router.post('/posts/', response_model=PostResponse,
             status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    use_case: CreatePostUseCase = Depends()
) -> PostResponse:
    try:
        return await use_case.execute(post_data=post_data)
    except UserNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
    except LocationNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )


@router.put('/posts/{post_id}', response_model=PostResponse,
            status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    use_case: UpdatePostUseCase = Depends()
) -> PostResponse:
    try:
        return await use_case.execute(post_id=post_id, post_data=post_data)
    except PostNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
    except LocationNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )


@router.delete('/posts/{post_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    use_case: DeletePostUseCase = Depends()
) -> None:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
