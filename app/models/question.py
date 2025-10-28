from tortoise import field
from tortoise.models import Model


class Question(Model):
    id = field.IntField(pk=True)
    content = field.TextField()
    
    class Meta:
        table = "qusetion"
    
    def __str__(self):
        return self.question_text[:30]
