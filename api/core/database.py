from core.settings import SETTINGS

TORTOISE_ORM = {
    "connections": {"default": SETTINGS.psql_url},
    "apps": {
        "models": {
            "models": ["aerich.models", "v1.auth.models", "v1.news.models"],
            "default_connection": "default",
        },
    },
    "timezone": "Europe/Warsaw",
}
