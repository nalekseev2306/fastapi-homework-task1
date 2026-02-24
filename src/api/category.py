from fastapi import APIRouter, status, HTTPException
from typing import List

from schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate

router = APIRouter()


categories_db = {} # тут будем временно хранить данные
category_counter = 1 # генератор id

# запросы к категориям
@router.category('/categories/', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate):
    pass

@router.get('/categories/', response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories():
    pass

@router.get('/categories/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category(category_id: int):
    pass

@router.put('/categories/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(category_id: int, category_update: CategoryUpdate):
    pass

@router.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int):
    pass
