from tortoise import fields
from tortoise.models import Model
from tortoise.fields import CharField, IntField, ForeignKeyField, DatetimeField


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    date = fields.DateField(null=True)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    author = fields.ForeignKeyField("models.User", related_name="posts")

    class Meta:
        table = "post"

    def __str__(self):
        return self.title
