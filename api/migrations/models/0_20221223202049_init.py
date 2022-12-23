from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "auth__role" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "auth__user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "first_name" VARCHAR(50),
    "last_name" VARCHAR(50),
    "password_hash" VARCHAR(128),
    "disabled" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "auth__user_role" (
    "auth__user_id" INT NOT NULL REFERENCES "auth__user" ("id") ON DELETE CASCADE,
    "role_id" INT NOT NULL REFERENCES "auth__role" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
