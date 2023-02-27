from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "news__bank_currency" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "bank_name" VARCHAR(255),
    "city_name" VARCHAR(7),
    "usd_buy" DECIMAL(4,3),
    "usd_sell" DECIMAL(4,3),
    "euro_buy" DECIMAL(4,3),
    "euro_sell" DECIMAL(4,3),
    "rub_buy" DECIMAL(4,3),
    "rub_sell" DECIMAL(4,3),
    "usd_buy_from_euro" DECIMAL(5,3),
    "usd_sell_from_euro" DECIMAL(5,3),
    CONSTRAINT "uid_news__bank__bank_na_187532" UNIQUE ("bank_name", "city_name")
);
COMMENT ON TABLE "news__bank_currency" IS 'Bank actual currency info';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "news__bank_currency";"""
