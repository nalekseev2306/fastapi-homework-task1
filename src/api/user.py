from fastapi import APIRouter, status, HTTPException
from typing import List

from schemas.user import UserResponse, UserCreate, UserUpdate

router = APIRouter()


users_db = {} # тут будем временно хранить данные
user_counter = 1 # генератор id

# запросы к пользователю
@router.post('/users/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    global user_counter

    new_user = {
        'id': user_counter,
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    users_db[user_counter] = new_user
    user_counter += 1

    return new_user

@router.get('/users/', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users():
    return list(users_db.values())

@router.get('/users/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    user = users_db.get(user_id)

    if not user:
        raise HTTPException(404, detail='User not found')
    
    return user

@router.put('/users/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_update: UserUpdate):
    user = users_db.get(user_id)

    if not user:
        raise HTTPException(404, detail='User not found')
    
    updated_user = {
        'id': user_id,
        'username': user_update.username if user_update.username is not None else user['username'],
        'email': user_update.email if user_update.email is not None else user['email'],
        'password': user_update.password if user_update.password is not None else user['password'],
        'first_name': user_update.first_name if user_update.first_name is not None else user['first_name'],
        'last_name': user_update.last_name if user_update.last_name is not None else user['last_name']
    }

    users_db[user_id] = updated_user
    return updated_user

@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    user = users_db.get(user_id)

    if not user:
        raise HTTPException(404, detail='User not found')
    
    del users_db[user_id]
    return None
