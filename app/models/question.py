from tortoise import fields
from tortoise.models import Model


class Question(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    answer = fields.TextField(null = True)

    class Meta:
        table = "question"

    def __str__(self):
        return self.content[:30]
