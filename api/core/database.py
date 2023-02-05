from core.settings import Settings, get_settings

settings: Settings = get_settings()


TORTOISE_ORM = {
    "connections": {"default": settings.get_psql_url()},
    "apps": {
        "models": {
            "models": ["aerich.models", "v1.auth.models", "v1.news.models"],
            "default_connection": "default",
        },
    },
    "timezone": "Europe/Warsaw",
}
