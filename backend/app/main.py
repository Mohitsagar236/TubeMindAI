from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import models  # noqa: F401 - registers ORM metadata
from .api import chat_routes, flashcard_routes, health_routes, history_routes, notes_routes, quiz_routes, settings_routes, video_routes
from .config import Settings, get_settings
from .container import build_container
from .database import Base, engine
from .exceptions import ServiceError


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(bind=engine)
        yield

    app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
    app.state.settings = settings
    app.state.services = build_container(settings)
    explicit_origins = [origin for origin in settings.cors_origin_list if "*" not in origin]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=explicit_origins,
        allow_origin_regex=r"chrome-extension://.*",
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-OpenAI-API-Key"],
    )

    @app.exception_handler(ServiceError)
    async def service_error_handler(_: Request, exc: ServiceError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    for router in (
        health_routes.router,
        video_routes.router,
        chat_routes.router,
        notes_routes.router,
        quiz_routes.router,
        flashcard_routes.router,
        history_routes.router,
        settings_routes.router,
    ):
        app.include_router(router, prefix="/api")
    return app


app = create_app()
