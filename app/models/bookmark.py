from tortoise import fields
from tortoise.models import Model


class Bookmark(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="bookmarks")
    quote = fields.ForeignKeyField("models.Quote", related_name="bookmarked_by")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "bookmark"
        unique_together = ("user", "quote")

    def __str__(self):
        return f"Bookmark(user={self.user_id}, quote={self.quote_id})"
