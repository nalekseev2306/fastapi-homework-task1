from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.user import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")

    # настройки (* - разрешает всё)
    app.add_middleware(
        CORSMiddleware, # type: ignore
        allow_origins=["*"], # с каких айпи разрешен запрос
        allow_credentials=True, # разрешение на использование токенов
        allow_methods=["*"], # какие методы разрешены
        allow_headers=["*"], # фильтр хэдеров
    )

    # подключаем роутеры
    app.include_router(router=user_router, prefix='/api', tags=['users'])

    return app
