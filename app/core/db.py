# app/core/db.py
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            # 모델 경로 목록 + (aerich 사용할 경우) "aerich.models"
            "models": [
                "app.models.user",
                "app.models.diary",
                "app.models.quote",
                "app.models.question",
                "app.models.questions",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}
