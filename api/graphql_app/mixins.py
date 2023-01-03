from typing import Any

from auth import models as auth_models
from auth.dependencies import get_authenticated_user


class ContextUserMixin:
    @staticmethod
    async def _get_user(context: dict[str, Any]) -> auth_models.User:
        user: auth_models.User | None = await get_authenticated_user(context["request"])
        context["user"] = user
        return user
