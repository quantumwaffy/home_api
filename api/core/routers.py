import dataclasses

from fastapi import APIRouter
from v1.auth.router import router as auth_router
from v1.graphql_app.router import router as graphql_router
from v1.news.router import router as news_router


@dataclasses.dataclass
class AppRouter:
    v1: tuple[APIRouter, ...] = (auth_router, news_router, graphql_router)

    @classmethod
    @property
    def routers(cls) -> tuple[tuple[str, tuple[APIRouter, ...]], ...]:
        return tuple(
            [
                (f"/api/{f_name}", f_obj.default)
                for f_name, f_obj in cls.__dataclass_fields__.items()
                if not f_name.startswith("_")
            ]
        )
