from tortoise import fields
from tortoise.models import Model


class Questions(Model):
    content = fields.TextField()

    class Meta:
        table = "questions"

    def __str__(self):
        return self.content[:30]
