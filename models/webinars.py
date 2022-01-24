from tortoise import fields
from tortoise.models import Model


class Webinars(Model):
    uid = fields.UUIDField(pk=True)
    text = fields.TextField()

    def __str__(self):
        print(self.uid)
