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
    "post_id" INT NOT NULL UNIQUE REFERENCES "post" ("id") ON DELETE CASCADE
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
    "FL1nxB4bwYn8c+Pg/H+WkF2IU+eX6K8TwA4dz6t/XTQiCA7CGje9qywGKhNFxAwdgXxmPd"
    "akxoCBzK5BPgE8hELiRO6C2ohxGTosj3uRA7zNBDUyWKkHcbQZviKaQzGDLF9bUVEfbElL"
    "cRptC6uWGPHnLhHSRcz78u5vbEg76bmL/ncicht+lqIWTniJ4JQ/7zY9vBfhQgZbxY0RlG"
    "W2sPUS6dQgRDQCEfnoYRj4dPNw5dhriZujLZTFHzceEERD7V4t8RFAcjDiibDREBTvmvPG"
    "u/OHl18vqflyevmYmYyVbyar0JT8W+cRQIDEbWWugBBRsLAaPCzQkhD9YGNIvfG6ahXgDN"
    "ICY9U2C6setz+ZCGVgJZhK0UKHDVDtsTuiwGd4j8VbxwBVCOzi/6V6PuxUceSUDIrS8g6o"
    "76XNMW0lVKevTyCZdjlh+bxNkO0vp6Pnrb4l9b34eDvkAQEzoNxS8qu9F3i88JRBTbCC9t"
    "4Gp7TEolMMxSLazIH7tUWuguv06OiqzgXvJDwcaPn3KoaR6PCTR+Ek/mxjNFHuFJAM9wCL"
    "0peg9XAsdzNiOAHGjALa5Fn+NhqoffWu4BKVU5GYLltjrpW4OFx4KCVATY6171um/6VjZh"
    "9wDbJzlOfXHTDyIzcHz3jYEzX4LQtRPbkGtwG6ckW9usKmgHaQlAYCoA4GHwScfQfmRHtI"
    "k1CXkhY1pIi72ypYYcHZYcUY/6hpTszUBoxm7rkIKPTbqaGcn2+p3tQzSlM/b1xfFxAV5f"
    "upe9t93LI2aVojWDWNXe6JIVlTNAM7c0YyjtixjlDmDGW+3hTzcTdJwQpmBhzhQiA+sewb"
    "uczNRc6rK/igh1/9sowaXlLjq66H57kuDTH4aD/6S5tut6H4anaVSbvzN/598Zppzhksw8"
    "4dNwcw3Hhp2nt8dBaaZO8iER8WQW4DR2HSI4wuzjEvpAWuYRfTVWVYthZhHWJSn3NkgD7d"
    "YByKfeOuQN/a7aUVVEvxuKdAiKBBBZmvoz+aAqj9/CtFJM/CCQcq5TjppoHvshJnXI9Qwt"
    "KVNek2hnoZZ1c0f6Ils2VcN5V/KibaAdqMu9ul6yzJKiGkx2K8KkqcJVzMymCj9EybjX+b"
    "fPfMbirDDkcnxzUJTH0mTP1/7qf2kACWETb67+D53Yea2A/Pa28qhLWj9AfztuIyxCPPHK"
    "3RZkPWvCr5OotndCtV2AajuLqjwFSlQdzaUu27NiVUfBL9/wgq49XuU3q87e/7pNpb9SVt"
    "kVMPepDlWBRe/UUIBlTzW//spXKxoKXadKy1dNPJcoDrrPfo6zg6OYqAqdXYpCJ78mdDIl"
    "wcdTDxnbLPko6j57Ka51B3EGyIwd6gtAyBKHpbA0uNalzqYIS6ezC2HpdPIJC9c1N8+P4u"
    "YZRcEYhjae2HxgUqICGjwf7hb6+M+Ww3uxTgPIj4Bxpm8U7onC73a4/1LO3YWh58wsA+uO"
    "NYW8GyibhnnXiHn/gCExvm6RT3M0l4beqC4XS40SIMbm9QTwIG3C3GuUd1fDQdlrlM+IBX"
    "jteg592vI9Qm+qCWsBijzq4vZWupOVYnZ8gD9+qbL+H0/Sbv0="
)
