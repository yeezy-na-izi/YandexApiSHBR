from tortoise import fields
from tortoise.models import Model


class Node(Model):
    id = fields.CharField(pk=True, max_length=100)
    type = fields.CharField(max_length=10)
    parent = fields.ForeignKeyField(
        model_name="models.Node",
        related_name="children",
        null=True,
    )
    size = fields.IntField(null=True)
    url = fields.CharField(max_length=255, null=True)
    date = fields.DatetimeField()


class NodeHistory(Model):
    id = fields.UUIDField(pk=True)
    node = fields.ForeignKeyField(
        model_name="models.Node",
        related_name="history",
    )
    type = fields.CharField(max_length=10)
    parent = fields.ForeignKeyField(
        model_name="models.Node",
        related_name="children_history",
        null=True,
    )
    size = fields.IntField()
    url = fields.CharField(max_length=255, null=True)
    date = fields.DatetimeField()
