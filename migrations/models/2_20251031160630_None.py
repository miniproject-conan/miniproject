from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
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
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "question" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "answer" TEXT,
    "post_id_id" INT NOT NULL UNIQUE REFERENCES "post" ("id") ON DELETE CASCADE
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


MODELS_STATE = (
    "eJztWm1v2joU/isonzppmzpu2ab7jTJ6122FrWUvWlVFJjEQkdg0dkbRxH+/tomxkzgZWa"
    "FL1nxB4bw4Pk98fJ4c56cVYBf65PkpxvMAhHPr39ZPC4EAsouM7mnLAouF0nABBWNfGI91"
    "qzGhIXAok0+ATyATuZA4obegHkZMiiLf50LsMEMPTZUoQt5tBG2Kp5DOYMgU19dWRNgVU9"
    "5GmELr5oZdesiFd5BwPf+7mNsTD/puYv6ey52E3KarhZCdI3omDPntx7aD/ShAynixojOM"
    "ttYeolw6hQiGgEI+PA0jHg+fbhy6DHEzdWWymaLm48IJiHyqxb8jKA5GHFA2GyICnPK7PG"
    "u/OHl18vqflyevmYmYyVbyar0JT8W+cRQIDEbWWugBBRsLAaPCzQkhD9YGNIvfG6ahXgDN"
    "ICY9U2C6setzeZGGVgJZhK0UKHDVCtsTuiwGd4j8VfzgCqAcnV/0r0bdi488koCQW19A1B"
    "31uaYtpKuU9OjlEy7HLD82ibMdpPX1fPS2xf+2vg8HfYEgJnQaijsqu9F3i88JRBTbCC9t"
    "4GprTEolMMxSPViRP3aptNBdfp0cFXmCe8kPBRvffsqhpnk8JtD4TjyZG/cUuYUnATzDIf"
    "Sm6D1cCRzP2YwAcqABt7gWfY6HqR5+a7kGpFTlZAiW2+qkLw0WHgsKUhFgr3vV677pW9mE"
    "3QNsn+Q49cVN34jMwPHVNwbOfAlC104sQ67BbZySbG2zqqAdpCUAgakAgIfBJx1D+5Ft0S"
    "bWJOSFjGkhLfbKlhpydFhyRD3qG1KyNwOhGbutQwo+NulqZiRb63e2D9GUztjfF8fHBXh9"
    "6V723nYvj5hVitYMYlV7o0tWVM4AzdzSjKG0L2KUO4AZL7WH391M0HFCmIKFOVOIDKx7BO"
    "9yMlNzqcv6KiLU/W+jBJeWq+joovvtSYJPfxgO/pPm2qrrfRieplFtXmf+ztcZppzhksw8"
    "4dNwcw3Hhp2nl8dBaaZO8iER8WQewGnsOkRwhNnPJfSBtMwj+mqsqhbDzENYl6Tc2yANtF"
    "sHIJ9665A39LtqW1UR/W4o0iEoEkBkaerP5IOqPH4L00ox8YNAyrkOqyPl2EnSaT/0pA4Z"
    "nyEnZYpsBvMs4LKA7shjZO+malDvymKSy2gHGnOvDpgsuaSoHpPdCjJpKnIV87OpyA9RPu"
    "61C+4zn7HYKwy5HJ8iFOWxNNnzJwDqHTWAhLCJN58BHDqx89oC+a1u5VGXtH6AXnfcUliE"
    "eOKVOznIetaEaydRbe+EarsA1XYWVbkLlKg6mktdlmfFqo6CX37tBV17vMpvXJ29/3XLSv"
    "+8rLJPwNyzOlQFFn1UQwGW/dX8+is/s2godJ0qLX9q4rpEcdB99rOdHRzFRFXo7FIUOvk1"
    "oZMpCT6eesj4+p+Pou6zl+JadxBngMzYpr4AhCxxWApLg2td6myKsHQ6uxCWTiefsHBdcw"
    "r9KE6hURSMYWjjic0HJiUqoMHz4U6kj/9sObwX6zSA/AgYZ/p04Z4o/G6T+y/l3F0Yes7M"
    "MrDuWFPIu4GyaZh3jZj3DxgS46cX+TRHc2nojepysdQoAWJsXk8AD9ImzD1GeXc1HJQ9Rv"
    "mMWIDXrufQpy3fI/SmmrAWoMijLm5vpTtZKWbHB/jjhyrr/wFe0nOt"
)
