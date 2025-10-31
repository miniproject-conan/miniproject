from tortoise import fields
from tortoise.models import Model


class Question(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    answer = fields.TextField(null = True)

    post = fields.OneToOneField("models.Post", related_name="question", on_delete="CASCADE")

    class Meta:
        table = "question"

    def __str__(self):
        return self.content[:30]
