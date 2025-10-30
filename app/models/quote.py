from tortoise import fields
from tortoise.models import Model


class Quote(Model):
    id = fields.IntField(pk=True)
    author = fields.CharField(max_length=100)
    author_profile = fields.CharField(max_length=200, null=True)
    message = fields.TextField()

    class Meta:
        table = "quote"
        unique_together = ("author", "message")

    def __str__(self):
        return f"{self.author}: {self.message[:30]}"
