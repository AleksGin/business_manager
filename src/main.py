from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.models import db_helper
from users.routers import (
    auth_router,
    users_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.engine_dispose()


def create_app() -> FastAPI:
    """Фабрика для создания FastAPI приложения"""

    app = FastAPI(
        title="Business Managment System",
        description="MVP система управления командами и задачами",
        version="1.0",
        lifespan=lifespan,
    )

    # CORS middleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаем роутеры
    app.include_router(
        auth_router,
        prefix=settings.api_prefix.auth,
        tags=["Аутентификация"],
    )

    app.include_router(
        users_router,
        prefix=settings.api_prefix.user,
        tags=["Пользователи"],
    )

    @app.get("/")
    async def root():
        """Главная страница"""
        return {"message": "Business Manager", "docs": "/docs", "version": "1.0"}

    @app.get("/health")
    async def health_check():
        """Проверка здоровья приложения"""
        return {"status": "ok"}

    return app


# Создание экземпляра приложения
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.app_config.host,
        port=settings.app_config.port,
        reload=settings.app_config.reload_mode,
    )
