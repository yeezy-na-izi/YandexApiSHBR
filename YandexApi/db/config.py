MODELS_PATH = "YandexApi.db.models."
MODELS_MODULES: list[str] = [MODELS_PATH + model for model in ["node"]]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": "sqlite://production-database.sqlite3",
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
