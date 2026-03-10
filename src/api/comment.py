from typing import List
from fastapi import APIRouter, status, Depends

from schemas.comment import CommentResponse, CommentCreate, CommentUpdate
from domain.comment.use_cases import *

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
    return await use_case.execute(comment_id=comment_id)


@router.post('/comments/', response_model=CommentResponse,
             status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    use_case: CreateCommentUseCase = Depends()
) -> CommentResponse:
    return await use_case.execute(comment_data=comment_data)


@router.put('/comments/{comment_id}', response_model=CommentResponse,
            status_code=status.HTTP_200_OK)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    use_case: UpdateCommentUseCase = Depends()
) -> CommentResponse:
    return await use_case.execute(comment_id=comment_id, comment_data=comment_data)


@router.delete('/comments/{comment_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends()
) -> None:
    return await use_case.execute(comment_id=comment_id)
