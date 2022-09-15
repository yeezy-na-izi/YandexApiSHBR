from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from tortoise.contrib.fastapi import register_tortoise

from YandexApi.db.config import TORTOISE_CONFIG
from YandexApi.web.api.router import api_router
from YandexApi.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="YandexApi",
        description="Task For SHBR",
        version=metadata.version("YandexApi"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router)
    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
        generate_schemas=True,
    )

    return app
