from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_quote_author_c1bb3f" ON "quote" ("author", "message");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_quote_author_c1bb3f";"""


MODELS_STATE = (
    "eJztWm1v0zoU/itVPg0J0OhdAfGtK91lwFrYyouYpshN3DRqYmexw1ah/ndsN66dxMltuO"
    "1oIN/S85L4PDk+5/FJf1ghdmFAnp5ivAhBvLBedX5YCISQXRR0jzsWiCKl4QIKpoEwnupW"
    "U0Jj4FAmn4GAQCZyIXFiP6I+RkyKkiDgQuwwQx95SpQg/zaBNsUepHMYM8X1tZUQdsWUtw"
    "mm0Lq5YZc+cuE9JFzPf0YLe+bDwM2s33e5k5DbdBkJ2TmiZ8KQP35qOzhIQqSMoyWdY7Sx"
    "9hHlUg8iGAMK+e1pnPB4+HLT0GWI66Urk/USNR8XzkASUC3+LUFxMOKAstUQEaDHn/Kk++"
    "zkxcnLf56fvGQmYiUbyYvVOjwV+9pRIDCaWCuhBxSsLQSMCjcnhjxYG9Aifq+ZhvohNIOY"
    "9cyB6aauT+VFHloJZBW2UqDAVRm2I3RZDO4YBcv0xVVAOTm/GF5N+hcfeCQhIbeBgKg/GX"
    "JNV0iXOenR80dcjtn+WG+czU06X84nbzr8Z+fbeDQUCGJCvVg8UdlNvll8TSCh2Eb4zgau"
    "lmNSKoFhlurFiv1j19oWust/b44DeYM72R8KNl5+6qGmefxNoPFKPFsYa4os4VkAz3AMfQ"
    "+9g0uB4zlbEUAONOCW9qJP6W0OD7+VzAEpVXsyBneb7qSnBguPBQWpCHDQvxr0Xw+t4obd"
    "AWwf5X2ai5teiMzA8eybAmdxB2LXzqQh1+Auzkk2tkVV2A3zEoCAJwDgYfBFp9B+YCXaxJ"
    "qEvJIxRdJip2ypJUf7JUfUp4FhSw7mIDZjt3HIwccWfZg7kuX6vR1A5NE5+/ns+LgCr8/9"
    "y8Gb/uURs8rRmlGq6q512Y7KGaCZW5oxlPZVjHILMNNUe/jqZoKOE8IcLMyZQmRg3RN4X7"
    "IzNZem5FcVoR5+nWS4tMyio4v+10cZPv1+PPpXmmtZN3g/Ps2j2h5n/szjDFPOcU1mnvFp"
    "ubmGY8vO8+lxSDTzYwJJGnSBam50lXTzVrdqKeeBbc8qyinfnE0ZDahDPQuOTaEIWQra7f"
    "W2oKDMqpSCCl3LCv5YVlBobr+rSGPRLAwVOp2/VJVnabLjjyequ4eQELbw9gPKvgt2GaEq"
    "r9TKo5klei9TgpSMRTGe+fVmLkXPX4L14ecFuca3FardClS7RVRlFSjAWT5k0Fyakp4PMW"
    "So0XUU/PI7OSMQ02XxJZym7mfvLmEAJF83H7f0D/MH+wYKR67VPjuwOIEaGrA8mZb3X/mB"
    "qj0aNanT8rcmrms0B91nN+Vs7yhmukJvm6bQK+8JvUJLCLDnI+McrRxF3WcnzbXpIM4Bmb"
    "OiHgFC7nBcC0uDa1P6bHtSb0/qvzq/R0k4hbGNZza/ManRAQ2eDzfLP/697fB/sU4DyH8B"
    "49STriTV6qAg/9rRIAT2ybn7MPaduWVg3ammkncDZdMy7wYx7+8wJuku2ZbmaC4tvVFTLr"
    "Y1aoCYmjcTwL2MCUv/NfP2ajyq+6+ZT4gFeO36Dn3cCXxCbw4T1goUedTV4638JCvH7PgN"
    "ao63dt9eVj8BeURC0g=="
)
