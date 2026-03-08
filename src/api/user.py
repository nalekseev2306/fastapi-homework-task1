from typing import List
from fastapi import APIRouter, status, Depends

from schemas.user import UserResponse, UserCreate, UserUpdate
from domain.user.use_cases import *


router = APIRouter()


@router.get('/users/', response_model=List[UserResponse],
            status_code=status.HTTP_200_OK)
async def get_all_users(
    use_case: GetUsersUseCase = Depends()
) -> List[UserResponse]:
    return await use_case.execute()


@router.get('/users/{user_id}', response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends()
) -> UserResponse:
    return await use_case.execute(user_id=user_id)


@router.get('/users/by-username/{username}', response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends()
) -> UserResponse:
    return await use_case.execute(username=username)


@router.get('/users/by-email/{email}', response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def get_user_by_email(
    email: str,
    use_case: GetUserByEmailUseCase = Depends()
) -> UserResponse:
    return await use_case.execute(email=email)


@router.post('/users/', response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUserUseCase = Depends()
) -> UserResponse:
    return await use_case.execute(user_data=user_data)


@router.put('/users/{user_id}', response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_case: UpdateUserUseCase = Depends()
) -> UserResponse:
    return await use_case.execute(user_id=user_id, user_data=user_data)


@router.delete('/users/{user_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends()
) -> None:
    return await use_case.execute(user_id=user_id)
