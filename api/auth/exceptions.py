from fastapi import HTTPException, status

credentials_error: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

authentication_error: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
signup_user_exists: HTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User with this username already exists",
)

no_user: HTTPException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Could not find user",
)

access_token_expired: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired",
    headers={"WWW-Authenticate": "Bearer"},
)
