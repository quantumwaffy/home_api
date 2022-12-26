from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from . import utils
from .schemas import Token

router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):  # noqa
    return Token(access_token=await utils.Authenticator.create_access_token(form_data.username, form_data.password))
