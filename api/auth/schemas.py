import datetime
import string

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, root_validator, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from . import consts, models

UserDB = pydantic_model_creator(models.User, name="User")
UserView = pydantic_model_creator(models.User, name="UserView", exclude_readonly=True, exclude=("disabled",))


class NewUser(UserView):
    password_hash: str = Field(min_length=8, max_length=50, regex=consts.PASSWORD_REGEX, alias="password")
    confirm_password: str

    @root_validator()
    def verify_password_match(cls, values: dict[str, str]) -> dict[str, str]:
        password = values.get("password_hash")
        confirm_password = values.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValueError("The two passwords did not match.")
        return values

    @validator("password_hash")
    def validate_password_security(cls, password: str) -> str:
        if not any(char in consts.PASSWORD_REGEX for char in password):
            raise ValueError("Password must contain at least one specific character")
        if not any(char in string.digits for char in password):
            raise ValueError("Password must contain at least one numeric character")
        if not any(char in string.ascii_letters for char in password):
            raise ValueError("Password must contain at least one ascii character")
        if not any(char in string.ascii_lowercase for char in password):
            raise ValueError("Password must contain at least one ascii character in lowercase")
        if not any(char in string.ascii_uppercase for char in password):
            raise ValueError("Password must contain at least one ascii character in uppercase")
        return password


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="JWT")


class TokenGeneratedData(BaseModel):
    access_token: str
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class JWTPayload(BaseModel):
    expiry_date: int | datetime.datetime = Field(alias="exp")
    username: str = Field(alias="sub")

    @validator("expiry_date")
    def validate_expiry_date(cls, exp_timestamp: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(exp_timestamp)
