from tortoise import fields
from tortoise.models import Model


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    date = fields.DateField(null=True)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.User", related_name="posts")
    question = fields.OneToOneField("models.Question", related_name="post", null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "post"

    def __str__(self):
        return self.title
