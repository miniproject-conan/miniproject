from app.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.bookmark",
                "app.models.diary",
                "app.models.question",
                "app.models.questions",
                "app.models.quote",
                "app.models.user",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "Asia/Seoul",
}
