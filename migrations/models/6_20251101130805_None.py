from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "question" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "answer" TEXT
);
CREATE TABLE IF NOT EXISTS "questions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "quote" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "author" VARCHAR(100) NOT NULL,
    "author_profile" VARCHAR(200),
    "message" TEXT NOT NULL,
    CONSTRAINT "uid_quote_author_c1bb3f" UNIQUE ("author", "message")
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "login_id" VARCHAR(50) UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "number_of_posts" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "bookmark" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "quote_id" INT NOT NULL REFERENCES "quote" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_bookmark_user_id_46416a" UNIQUE ("user_id", "quote_id")
);
CREATE TABLE IF NOT EXISTS "post" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "date" DATE,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "question_id" INT UNIQUE REFERENCES "question" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
