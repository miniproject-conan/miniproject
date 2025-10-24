from tortoise import fields
from tortoise.models import Model


class Quote(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
