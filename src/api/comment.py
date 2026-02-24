from fastapi import APIRouter, status, HTTPException
from typing import List

from schemas.comment import Comment

router = APIRouter()


comments_db = {} # тут будем временно хранить данные
comment_counter = 1 # генератор id, но для каждого поста должен быть свой набор id?

# запросы к комментариям
@router.post('/posts/{post_id}/comments/', response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: int, post: Comment):
    pass

@router.get('/posts/{post_id}/comments/', response_model=List[Comment], status_code=status.HTTP_200_OK)
async def get_all_comments(post_id: int):
    pass

@router.get('/posts/{post_id}/comments/{comment_id}', response_model=Comment, status_code=status.HTTP_200_OK)
async def get_comment(post_id: int, comment_id: int):
    pass

@router.put('/posts/{post_id}/comments/{comment_id}', response_model=Comment, status_code=status.HTTP_200_OK)
async def update_comment(post_id: int, comment_id: int, comment_update: Comment):
    pass

@router.delete('/posts/{post_id}/comments/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(post_id: int, comment_id: int):
    pass
