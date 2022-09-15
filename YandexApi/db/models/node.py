from tortoise import fields
from tortoise.models import Model


class Node(Model):
    id = fields.UUIDField(pk=True)
    type = fields.CharField(max_length=10)
    parent = fields.ForeignKeyField(
        model_name="models.Node",
        related_name="children",
        null=True,
    )
    size = fields.IntField(null=True)
    url = fields.CharField(max_length=255, null=True)
    date = fields.DatetimeField()
