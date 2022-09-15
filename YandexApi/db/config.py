from YandexApi.settings import settings

MODELS_PATH = "YandexApi.db.models."
MODELS_MODULES = [MODELS_PATH + model for model in ["node"]]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": settings.db_url,
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
