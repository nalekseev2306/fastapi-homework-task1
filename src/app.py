from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import (
    user_router, post_router, category_router,
    comment_router, location_router
)


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
    app.include_router(router=user_router, tags=['users'])
    app.include_router(router=post_router, tags=['posts'])
    app.include_router(router=category_router, tags=['categories'])
    app.include_router(router=location_router, tags=['locations'])
    app.include_router(router=comment_router, tags=['comments'])

    return app
