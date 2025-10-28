from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "question" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "quote" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "author" VARCHAR(100) NOT NULL,
    "author_profile" VARCHAR(200),
    "message" TEXT NOT NULL
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
    "eJztWm1v0zoU/itVPg0J0OhdAfGtK91lwFrYyouYpshN3DRqYme2w1ah/ndsN26cxMltuO"
    "1oIN/S85L6PD4+5/Fpf1ghdmFAn55ivAgBWVivOj8sBELIHwq6xx0LRFGqEQIGpoE0nupW"
    "U8oIcBiXz0BAIRe5kDrEj5iPEZeiOAiEEDvc0EdeKoqRfxtDm2EPsjkkXHF9bcWUP3HlbY"
    "wZtG5u+KOPXHgPqdCLj9HCnvkwcDPr913hJOU2W0ZSdo7YmTQUXz+1HRzEIUqNoyWbY7Sx"
    "9hETUg8iSACD4vWMxCIesdwkdBXieumpyXqJmo8LZyAOmBb/lqA4GAlA+WqoDNAT3/Kk++"
    "zkxcnLf56fvOQmciUbyYvVOrw09rWjRGA0sVZSDxhYW0gYU9wcAkWwNmBF/F5zDfNDaAYx"
    "65kD001cn6qHPLQKyCpslSAFN82wHaHLY3DHKFgmG1cB5eT8Yng16V98EJGElN4GEqL+ZC"
    "g0XSld5qRHzx8JOebnY31wNi/pfDmfvOmIj51v49FQIogp84j8xtRu8s0SawIxwzbCdzZw"
    "tRxTUgUMt0w3Vp4fu9ax0F3++3AcyA7u5HyksInyUw81zeNvAk1U4tnCWFNUCc8CeIYJ9D"
    "30Di4ljud8RQA50IBb0os+Ja85PPxWKgeUND2TBNxtupOeGjw8HhRkMsBB/2rQfz20igd2"
    "B7B9VO9pLm56ITIDJ7JvCpzFHSCunUlDocFdnJNsbIuqsBvmJQABTwIgwhCLTqD9wEu0iT"
    "VJeSVjipTFTtlSS472S46YzwLDkRzMATFjt3HIwccXfZgnkuf6vR1A5LE5//js+LgCr8/9"
    "y8Gb/uURt8rRmlGi6q512Y4qGKCZW5oxVPZVjHILMJNUe/jqZoJOEMIcLNyZQWRg3RN4X3"
    "IyNZem5FcVoR5+nWS4tMqio4v+10cZPv1+PPpXmWtZN3g/Ps2j2l5n/szrDFfOcU1mnvFp"
    "ubmGY8vO8+lxSDTzYwxpEnSBam50lXTzVrdqKeeBHc8qyql2zmacBtShngXHplCELAXt9n"
    "pbUFBuVUpBpa5lBX8sKyg0t99VpLFsFoYKncxfqsqzMmlrc4Nqcxl3Ki/KqUczq/FeBgIJ"
    "74oInvn1xitFz1+C9eFHA7ketxWq3QpUu0VUQ0gpr1R15gmaS1PS8yHmCTUaTAq/+kmcc4"
    "XpsrgJp4n72btLGABFzc03K/03+IPdgcLtarXPZisvm4Zeqy6h5a1W/RbVdtomdVqxa/K5"
    "RnPQfXZTzvaOYqYr9LZpCr3yntArtIQAez4yjszKUdR9dtJcmw7iHNA5L+oRoPQOk1pYGl"
    "yb0mfbS3l7Kf/VUT2KwykkNp7Z4sW0Rgc0eD7c2P7497bD/8U6DSD/BYxTT7qSVKuDgvoX"
    "R4MQ2Cfn7kPiO3PLwLoTTSXvBqlNy7wbxLy/Q0KTU7ItzdFcWnqTTrn40agBYmLeTAD3Mi"
    "Ys/YPM26vxqO4fZD4hHuC16zvscSfwKbs5TFgrUBRRV4+38pOsHLMTL6g53tp9e1n9BItU"
    "O84="
)
