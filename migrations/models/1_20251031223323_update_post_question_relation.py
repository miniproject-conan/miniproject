from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "question" DROP CONSTRAINT IF EXISTS "fk_question_post_29339d68";
        ALTER TABLE "post" ADD "question_id" INT UNIQUE;
        ALTER TABLE "question" DROP COLUMN "post_id";
        ALTER TABLE "post" ADD CONSTRAINT "fk_post_question_d4b7bb1b" FOREIGN KEY ("question_id") REFERENCES "question" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" DROP CONSTRAINT IF EXISTS "fk_post_question_d4b7bb1b";
        ALTER TABLE "post" DROP COLUMN "question_id";
        ALTER TABLE "question" ADD "post_id" INT NOT NULL UNIQUE;
        ALTER TABLE "question" ADD CONSTRAINT "fk_question_post_29339d68" FOREIGN KEY ("post_id") REFERENCES "post" ("id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "eJztWu9v0zwQ/leqfBrSQKOsgN5vXelgwFrerbwgpilyE7eNmthd7NBVqP/7a7txnR9OSL"
    "Z2JDRfpux8l/oe3/mes/PL8LANXfLiDOO5B/y58U/rl4GAB9lDauy4ZYDFQo1wAQVjVyiP"
    "o1pjQn1gUSafAJdAJrIhsXxnQR2MmBQFrsuF2GKKDpoqUYCcuwCaFE8hnUGfDdzcGAFhT2"
    "zwLsAUGre37NFBNryHhI/zfxdzc+JA147N37G5kZCbdLUQsgtEz4Ui//mxaWE38JBSXqzo"
    "DKOttoMol04hgj6gkL+e+gH3h083dF26uJm6UtlMMWJjwwkIXBrxvyAoFkYcUDYbIhyc8l"
    "953n55+ub07avXp2+ZipjJVvJmvXFP+b4xFAgMRsZajAMKNhoCRoWb5UPurAloGr93bIQ6"
    "HtSDGLdMgGmHpi/kQxJaCWQetlKgwFURtiN0mQ/2ELmrcOFyoBxdXPavR93LL9wTj5A7V0"
    "DUHfX5SFtIVwnp0etnXI5ZfmwSZ/uS1reL0YcW/7f1YzjoCwQxoVNf/KLSG/0w+JxAQLGJ"
    "8NIEdiTGpFQCwzTVwor8MUulRdTk98lRkRXcSX4o2Pj2Uw61iMUhgcZ34slcu6fILTwO4D"
    "n2oTNFn+BK4HjBZgSQBTW4hbXoa/ia6uG3ljEgpSonfbDcVqdoaDD3mFOQCgd73ete913f"
    "SCfsDmD7V76nvrhFNyI9cDz6xsCaL4Fvm7Ew5CO4jROSrW56yGt7SQlAYCoA4G7wSYfQfm"
    "FbtI41CXkuY1pIjZ2ypYYc7ZccUYe6mpTszYCvx25rkICPTbqaGcli/d50IZrSGfv35clJ"
    "Dl7/da96H7pXR0wrQWsG4VB7MxavqJwB6rmlHkOpn8coC4AZhtrT72466DghTMDCjClEGt"
    "Y9gvcZmRkxqUt85RHq/vdRjEvLKDq67H5/FuPTn4eD91I9EnW9z8OzJKpNO/N3tjNscIZL"
    "MvOYzSFx8zithITPoWwrGLN6EHjJHbgObCCnq9lEU9PXJBPr8QQ9HaxplIcIjjD7U7gJUi"
    "+qWJgWb4JiKVgA5kf1NlvENP1NFM3sHie6eE2fU7Wd7TjvELjhonvgogCRpe4gLBtUZfEg"
    "TCvV8uwM0lRJ3tHZj1ooeTgTX6az0ExWnivoArm96YuOPAaq6jKlSs76gTWC5BUJUqxKkK"
    "ZMNGXiUMvEvva00vmMBZ/U5HJ4h5CXx1Jlxx8AqD7Lg4SwiTcfAew7sbNa2+yDbmVRl7R+"
    "gpPusC1e+HjilLs3SFvWhADGUW0XQrWdg2o7jarcBUpUnYhJXcKzYlVHwS+/9YK2OV5ls+"
    "TzT7/nx9GPyyq7AnqSvK8KLM4CNQVYnhFm11/5kUVDoetUafmqiecSxSFqs5vtbO8oxqpC"
    "p0hR6GTXhE6qJLh46ugvNLJRjNrspLjWHcQZIDO2qS8AIUvsl8JSY1qXOpsgLJ1OEcLS6W"
    "QTFj7W3EEfxB00Crwx9E08MfmLSYkKqLF8uvvokz9bDh/FOjUgHwDjjAZdRqiVQaHguXSV"
    "ENgn5+5C37FmhoZ1hyO5vBsonYZ514h5/4Q+0X5ZkE1zIiYNvVGnXCw1SoAYqtcTwL0cE2"
    "Zeo3y8Hg7KXqN8RczBG9ux6HHLdQi9rSasOShyr/OPt5InWQlmx1/wxy9V1v8DCptzfQ=="
)
