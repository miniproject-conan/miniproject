from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "qusetion" (
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
    "eJztWltz2jgU/iuMn9KZbieloe30jVCyzbaBNqG7nWYyHmEL48GWHEluwnT475WEhXyRvX"
    "gLCd74zZyLrfPpHJ1PEj+tELswoC9OMV6EgCysd52fFgIh5A8F3fOOBaJIa4SAgWkgjadp"
    "qyllBDiMy2cgoJCLXEgd4kfMx4hLURwEQogdbugjT4ti5N/G0GbYg2wOCVdcX1sx5U9ceR"
    "tjBq2bG/7oIxfeQyr04me0sGc+DNzM+H1XOEm5zZaRlJ0jdiYNxeentoODOETaOFqyOUYb"
    "ax8xIfUgggQwKF7PSCziEcNNQlchroeuTdZDTPm4cAbigKXi3xIUByMBKB8NlQF64it/dF"
    "+evDl5++r1yVtuIkeykbxZrcPTsa8dJQKjibWSesDA2kLCqHFzCBTB2oAV8XvPNcwPoRnE"
    "rGcOTDdxfaEe8tAqIKuwVQINrs6wHaHLY3DHKFgmE1cB5eT8Yng16V98FpGElN4GEqL+ZC"
    "g0XSld5qRHr58JOeb1sS6czUs6/5xPPnTEz8738WgoEcSUeUR+UdtNvltiTCBm2Eb4zgZu"
    "KseUVAHDLfXEyvqxa5VF2uXfi+NAZnAn9aFhE8tPPdRSHk8JNLESzxbGNUUt4VkAzzCBvo"
    "c+wqXE8ZyPCCAHGnBLetHX5DWHh99K5YCS6pok4G7TndKpwcPjQUEmAxz0rwb990OrWLA7"
    "gO2Lek9zcUsvRGbgRPZNgbO4A8S1M2koNLiLc5KNbVEVdsO8BCDgSQBEGGLQCbSf+RJtYk"
    "1SXsmYImWxU7bUkqP9kiPms8BQkoM5IGbsNg45+PigD7Miea7f2wFEHpvzny+Pjyvw+rt/"
    "OfjQvzziVjlaM0pU3bUu21EFAzRzSzOGyr6KUW4BZpJqD7+6maAThDAHC3dmEBlY9wTel1"
    "RmyqUp+VVFqIffJhkurbLo6KL/7VmGT38aj/5U5qmsG3wan+ZRbbcz/8/tDFfOcU1mnvFp"
    "uXkKx5ad59PjkGjmlxjSJOgC1dzoKunmLd95bKxaynlg5VlFOVtasCtaUFgEH6uYsVxUDJ"
    "Wc7NOryliZ7PiQXXeBEFLKB94etO+7sMsab/lmUns0pawfYDeZNO2I4Jlfb29e9PxPsD78"
    "vjKLancrVLsVqHaLqKpVoEbXSbk0JT0PrOto+NV9Kt9+TpfFSThN3M8+XsIAKF5npuXpC9"
    "yDnYECNV/tswPLnYqhAasdTHn/VRcZLYVuUqcVsyafazSHtM9ulrO9o5jpCr1tmkKvvCf0"
    "Ci0hwJ6PjOct5SimfXbSXJsO4hzQOV/UI0DpHSa1sDS4NqXP5ghLr7cNYen1ygmL0LXnvE"
    "/inBfF4RQSG89s8WJaowMaPB/uzPf4cdvhb7FOA8hPgHGmk64k1eqgoP4C0CAE9sm5+5D4"
    "ztwysO5EU8m7gbZpmXeDmPcPSGhSJdvSnJRLS2/0KRcvjRogJubNBHAvx4Sl1yh/XY1Hda"
    "9RviIe4LXrO+x5J/ApuzlMWCtQFFFXH2/lT7JyzE684NEvVVa/AC0kqgQ="
)
