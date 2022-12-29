from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from . import dependencies, exceptions, models, schemas, utils

router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.TokenGeneratedData)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):  # noqa
    return await utils.Authenticator.create_jwt_tokens(form_data.username, form_data.password)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserView)
async def sign_up(user_data: schemas.NewUser):
    if await models.User.filter(username=user_data.username).first():
        raise exceptions.signup_user_exists
    user_data.password_hash = utils.Authenticator.get_password_hash(user_data.confirm_password)
    user: models.User = await models.User.create(**user_data.dict(exclude={"confirm_password"}))
    return await schemas.UserView.from_tortoise_orm(user)


@router.get("/me", response_model=schemas.UserView)
async def get_me(user: models.User = Depends(dependencies.get_current_user)):  # noqa
    return user


@router.post("/refresh-token", response_model=schemas.AccessToken)
async def refresh_access_token(token: schemas.RefreshToken):
    return schemas.AccessToken(access_token=await utils.Authenticator.get_refreshed_access_token(token.refresh_token))
