import json
from typing import Any

from auth import dependencies as auth_deps
from auth import exceptions as auth_exc
from auth import schemas as auth_schemas
from fastapi import Depends
from starlette.requests import Request
from starlette.responses import Response
from strawberry.fastapi import GraphQLRouter

from . import schemas


async def get_context(user=Depends(auth_deps.get_current_user)) -> dict[str, auth_schemas.UserView]:  # noqa
    return {"user": user}


class BaseGraphQLRouter(GraphQLRouter):
    @staticmethod
    def _validate_status_code(response: Response) -> None:
        body_data: dict[str, Any] = json.loads(response.body)

        if not body_data.get("data") and (errors := body_data.get("errors")):
            exceptions_data: dict[str, int] = auth_exc.BaseAuthExceptionManager.http_exc_data
            error_codes: list[str | None] = [
                code for error in errors if (msg := error.get("message")) and (code := exceptions_data.get(msg))
            ]
            if error_codes:
                response.status_code = error_codes[-1]

    async def execute_request(self, request: Request, response: Response, data: dict, context, root_value) -> Response:
        response: Response = await super().execute_request(request, response, data, context, root_value)
        self._validate_status_code(response)
        return response


router: BaseGraphQLRouter = BaseGraphQLRouter(schemas.schema, path="/graphql")
