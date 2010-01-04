from django.db import models

from django.contrib.auth.models import User

class Task(models.Model):
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    created = models.DateTimeField()
    position = models.IntegerField()
    completed = models.BooleanField()


class TaskInterval(models.Model):
    task = models.ForeignKey(Task)
    doer = models.ForeignKey(User)
    started = models.DateTimeField()
    stopped = models.DateTimeField()
