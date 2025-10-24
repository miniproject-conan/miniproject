from tortoise import fields
from tortoise.models import Model

class Question(Model):
    id = fields.IntField(pk=True)
    question_text = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
