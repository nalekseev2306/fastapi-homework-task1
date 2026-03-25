from typing import List
from fastapi import APIRouter, status, Depends

from schemas.user import UserResponse, UserCreate, UserUpdate
from domain.user.use_cases import *
from core.exceptions.domain_exceptions import (
    UserNotFoundException,
    UserNotFoundByUsernameException,
    UserWithUsernameAlreadyExistException,
    UserNotFoundByEmailException,
    UserWithEmailAlreadyExistException
)
from core.exceptions.api_exceptions import (
    NotFoundByFieldException,
    AlreadyExistWithFieldException
)


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
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundException as exc:
        raise NotFoundByFieldException(exc)


@router.get('/users/by-username/{username}', response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends()
) -> UserResponse:
    try:
        return await use_case.execute(username=username)
    except UserNotFoundByUsernameException as exc:
        raise NotFoundByFieldException(exc)


@router.get('/users/by-email/{email}', response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def get_user_by_email(
    email: str,
    use_case: GetUserByEmailUseCase = Depends()
) -> UserResponse:
    try:
        return await use_case.execute(email=email)
    except UserNotFoundByEmailException as exc:
        raise NotFoundByFieldException(exc)


@router.post('/users/', response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUserUseCase = Depends()
) -> UserResponse:
    try:
        return await use_case.execute(user_data=user_data)
    except (UserWithUsernameAlreadyExistException,
            UserWithEmailAlreadyExistException) as exc:
        raise AlreadyExistWithFieldException(exc)


@router.put('/users/{user_id}', response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_case: UpdateUserUseCase = Depends()
) -> UserResponse:
    try:
        return await use_case.execute(user_id=user_id, user_data=user_data)
    except UserNotFoundException as exc:
        raise NotFoundByFieldException(exc)
    except (UserWithUsernameAlreadyExistException,
            UserWithEmailAlreadyExistException) as exc:
        raise AlreadyExistWithFieldException(exc)


@router.delete('/users/{user_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends()
) -> None:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundException as exc:
        raise NotFoundByFieldException(exc)
