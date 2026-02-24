from fastapi import APIRouter, status, HTTPException
from typing import List

from schemas.post import PostResponse, PostCreate, PostUpdate

router = APIRouter()


posts_db = {} # тут будем временно хранить данные
post_counter = 1 # генератор id

# запросы к постам
@router.post('/posts/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    pass

@router.get('/posts/', response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def get_all_posts():
    pass

@router.get('/posts/{post_id}', response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: int):
    pass

@router.put('/posts/{post_id}', response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_update: PostUpdate):
    pass

@router.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    pass
