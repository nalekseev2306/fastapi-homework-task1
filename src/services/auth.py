from typing import Annotated
from pydantic import SecretStr
from fastapi import Depends
from jose import JWTError, jwt

from core.exceptions.auth_exceptions import CredentialsException
from core.exceptions.database_exceptions import NotFoundException
from schemas.user import UserResponse
from resources.auth import oauth2_scheme
from infrastructure.sqlite.database import database as sqlite_database, Database
from infrastructure.sqlite.repositories import UserRepository

AUTH_EXCEPTION_MESSAGE = "Authorization data cannot be verified"
SECRET_AUTH_KEY = SecretStr("aF75A92Cd9s10KGL4nLdt1r85XRtZ7APNO6NheGeKdRBhhc9oObQywxmqPF")
AUTH_ALGORITHM = "HS256"


class AuthService:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        _database: Database = sqlite_database

        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[AUTH_ALGORITHM],
            )
            username: str = payload.get('sub')
            if username is None:
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
            
        with _database.session() as session:
            try:
                repo = UserRepository(session)
                user = repo.get_by_username(username=username)
            except NotFoundException:
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

            return UserResponse.model_validate(obj=user)           
