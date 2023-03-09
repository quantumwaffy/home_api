from typing import Any

from fastapi import HTTPException
from strawberry import BasePermission
from strawberry.types import Info
from v1.auth import models as auth_models

from . import mixins


class IsAuthenticated(mixins.ContextUserMixin, BasePermission):
    async def has_permission(self, source: Any, info: Info, **kwargs: dict[str, Any]) -> bool:
        try:
            user: auth_models.User | None = await self._get_user(info.context)
        except HTTPException as exc:
            user = None
            self.message = exc.detail
        return bool(user)
