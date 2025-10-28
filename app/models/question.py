from tortoise import fields
from tortoise.models import Model


class Question(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    
    class Meta:
        table = "qusetion"
    
    def __str__(self):
        return self.question_text[:30]
