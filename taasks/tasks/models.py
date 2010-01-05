from datetime import datetime

from django.db import models
from taasks.base.models import ExtUser

class Task(models.Model):
    creator = models.ForeignKey(ExtUser)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.now)
    position = models.IntegerField()
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title + (' (completed)' if self.completed else '')

class TaskInterval(models.Model):
    task = models.ForeignKey(Task)
    doer = models.ForeignKey(ExtUser)
    started = models.DateTimeField(default=datetime.now)
    duration = models.PositiveIntegerField(null=True)
