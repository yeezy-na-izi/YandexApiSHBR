from typing import List

from YandexApi.settings import settings

MODELS_MODULES: List[str] = []  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES,
            "default_connection": "default",
        },
    },
}
