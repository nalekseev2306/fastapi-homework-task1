from typing import List
from fastapi import APIRouter, status, Depends, HTTPException

from schemas.comment import CommentResponse, CommentCreate, CommentUpdate
from domain.comment.use_cases import *
from core.exceptions.domain_exceptions import (
    CommentNotFoundException,
    UserNotFoundException,
    PostNotFoundException
)

# придумать как связать комменты с конкретным постом
# router = APIRouter(prefix='/comments/{comment_id}')
router = APIRouter()


@router.get('/comments/', response_model=List[CommentResponse],
            status_code=status.HTTP_200_OK)
async def get_all_comments(
    use_case: GetCommentsUseCase = Depends()
) -> List[CommentResponse]:
    return await use_case.execute()


@router.get('/comments/{comment_id}', response_model=CommentResponse,
            status_code=status.HTTP_200_OK)
async def get_comment(
    comment_id: int,
    use_case: GetCommentUseCase = Depends()
) -> CommentResponse:
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )


@router.post('/comments/', response_model=CommentResponse,
             status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    use_case: CreateCommentUseCase = Depends()
) -> CommentResponse:
    try:
        return await use_case.execute(comment_data=comment_data)
    except UserNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
    except PostNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )


@router.put('/comments/{comment_id}', response_model=CommentResponse,
            status_code=status.HTTP_200_OK)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    use_case: UpdateCommentUseCase = Depends()
) -> CommentResponse:
    try:
        return await use_case.execute(comment_id=comment_id,
                                      comment_data=comment_data)
    except CommentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )


@router.delete('/comments/{comment_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends()
) -> None:
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
