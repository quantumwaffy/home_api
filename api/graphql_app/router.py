from auth import dependencies as auth_deps
from auth import schemas as auth_schemas
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter

from . import schemas


async def get_context(user=Depends(auth_deps.get_current_user)) -> dict[str, auth_schemas.UserView]:  # noqa
    return {"user": user}


router: GraphQLRouter = GraphQLRouter(schemas.schema, context_getter=get_context)
