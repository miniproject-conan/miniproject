from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "login_id" VARCHAR(50) UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "number_of_posts" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "post" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "title" VARCHAR(100) NOT NULL,
    "date" DATE,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "quote" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "author" VARCHAR(100) NOT NULL,
    "author_profile" VARCHAR(200),
    "message" TEXT NOT NULL,
    CONSTRAINT "uid_quote_author_c1bb3f" UNIQUE ("author", "message")
);
CREATE TABLE IF NOT EXISTS "qusetion" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmW1P2zAQx79K1VcgsQk6CmjvSimjA1oGZUMgFLmJm0YkdrCdQYX63Wc7cfMcWtSnsL"
    "5LznfJ3S++3L/pW9XBBrTp11sKSfV75a2KgAP5Qcy+U6kC1w2twsBA35aOnvLoU0aAzrht"
    "AGwKucmAVCeWyyyMuBV5ti2MWOeOFjJDk4esZw9qDJuQDWUeD4/cbCEDvkKqTt0nbWBB24"
    "ilaRni3tKusZErbW3ETqWjuFtf07HtOSh0dkdsiNHE20JMWE2IIAEMissz4on0RXZBlaoi"
    "P9PQxU8xEmPAAfBsFil3SgY6RoIfz4bKAk1xly+1vf3D/aNvB/tH3EVmMrEcjv3ywtr9QE"
    "mg06uO5TpgwPeQGENu4qnJ4xS95hCQbHzRmAREnnoSokK2UooOeNVsiEw25Kf13QJkvxvX"
    "zbPG9VZ9d1tUgvlW9vd3J1ipySVBNaRoY9NCWtYezKcYjfkQxYDRp4E4BHQIDc0FlL5gMh"
    "PLjND5bExlCKGG77RFUK3V61Ng5V65XOVaHKxOoChZAyzN9ISvMMuB2VzjkQmkRhD6VR2s"
    "KWBeg9FF9ijoiAK+vfZl66bXuLwSlTiUPtsSUaPXEis1aR0lrFsHiUcxuUjlT7t3VhGnlf"
    "tupyUJYspMIu8Y+vXuqyIn4DGsIfyiASPSvMqqwMQeLPKcPiQaHmjiwnSGCZgR+f44nNfz"
    "3F3tOBQaYvAUmYbC0Af60wsghhZbCVHnAD4Owk7Pr6ENZDVplIGEuuKXWM8WGavtoayqVQ"
    "QZXMN5rNJLTs1JWgACpsxa3FvcKYojQ2kqTPlK01UeG6VZIqXJLGbPJDMnAeUc5Xu70ygk"
    "7pU7yuVafJSLUZs9xLMZKv+i0f0Bqbm0V1IWOjF5kwoHIwZRhrzpwdeczoyElGV/FSmX1l"
    "0vJlrULtq6bNxtx4TLRbfzQ7lHdl3zonu80Y3/h27ki0NMMn+v5k6yWMzytOLqZ1pKLiY5"
    "piGeYgItE53DkWTZ5jkBpGe9iBNf19aPYJ405GYCXibyKL49eIG8LMj8Ad+4aTZO+Bs7X2"
    "YvUmb+8rDMI6Uz/YVCofk8cZmr0nyIbBwHUsoTrz5u5Odi5Wder+brzzCiLAJhCQI06HOX"
    "4IE1m5xPR87lq+fSv9BNRbVWQLWWpqreAjPo10hIWbbnMvTrDB93Fjt1IA3wZAyeYO2d2U"
    "PhxGvzoaNEk2bzY/STNXMDEksfZrVysFLYyCD02bRxidr4LyQ0eP9OK3EiIWVp4yX8/Sha"
    "Yxad6LuXE+BCNHfuQPl50+3MOlBuES/wwbB0tlOxLcoe1xNrAUVRdfF4SU6SnfgXNHGBlY"
    "+X8T8gmPw6"
)
