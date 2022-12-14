from fastapi.routing import APIRouter

from YandexApi.web.api import delete, echo, imports, nodes, updates, history

api_router = APIRouter()
api_router.include_router(imports.router)
api_router.include_router(nodes.router)
api_router.include_router(delete.router)
api_router.include_router(updates.router)
api_router.include_router(history.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
