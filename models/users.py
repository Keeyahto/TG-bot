from tortoise.models import Model
from tortoise import fields

class Users(Model):
    id = fields.CharField(max_length=20, pk=True)
    referals = fields.IntField()
    bought_courses = ''
    passing_subjects = fields.JSONField()
    starred_webs = fields.ManyToManyField('models.Courses', )