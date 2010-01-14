from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    STATUS_NEW = 1
    STATUS_DONE = 2
    STATUS_REMOVED = 3
    
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.now)
    position = models.IntegerField()
    status = models.IntegerField(default=STATUS_NEW)

    def __unicode__(self):
        return self.title

    def start(self, doer):
        # Stop the started tasks first
        started_intervals = TaskInterval.objects.filter(doer=doer,
            duration=None)
        now = datetime.now()
        for interval in started_intervals:
            interval.stop(now)
            interval.save()

        # Start this task
        interval = TaskInterval(task=self, doer=doer)
        interval.save()

    def stop(self, doer):
        # Find all started intervals for this task
        started_intervals = TaskInterval.objects.filter(task=self, doer=doer,
            duration=None)
        # Stop them
        now = datetime.now()
        for interval in started_intervals:
            interval.stop(now)
            interval.save()
            
    @property
    def is_done(self):
        return self.status == self.STATUS_DONE
        
    @property
    def is_removed(self):
        return self.status == self.STATUS_REMOVED
        

class TaskInterval(models.Model):
    task = models.ForeignKey(Task)
    doer = models.ForeignKey(User)
    started = models.DateTimeField(default=datetime.now)
    duration = models.PositiveIntegerField(null=True)

    def stop(self, now=None):
        if now is None:
            now = datetime.now()
        self.duration = (now - self.started).seconds
