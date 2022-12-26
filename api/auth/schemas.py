from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import User

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
