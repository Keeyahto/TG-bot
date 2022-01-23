from tortoise.models import Model
from tortoise import fields


class Webinars(Model):
    uid = fields.UUIDField(pk=True)
    text = fields.TextField()