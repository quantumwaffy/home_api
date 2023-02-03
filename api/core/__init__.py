from tortoise import Tortoise

Tortoise.init_models(
    ["auth.models", "news.models"],
    "models",
)
