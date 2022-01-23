from tortoise.models import Model
from tortoise import fields


class Courses(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(pk=True)
    subject = fields.CharField(max_length=64)
    school = fields.CharField(max_length=64)
    name = fields.CharField(max_length=64)
    month = fields.CharField(max_length=10)
    schedule_img_id = fields.TextField()
    webinars = fields.ManyToManyField('models.Webinars')

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return f'''{self.id}: name - {self.name},
             subject - {self.subject},
              school - {self.school},
               name - {self.name}'''
