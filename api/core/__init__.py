from tortoise import Tortoise

Tortoise.init_models(
    ["v1.auth.models", "v1.news.models"],
    "models",
)
