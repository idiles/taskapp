from datetime import datetime, timedelta
import re

from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.now)
    position = models.IntegerField()
    completed = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    due_date = models.DateField(null=True)

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
            
            
class TaskRegexp(object):
    """Helper class to extract date from task text."""
    
    MONTHS = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }
    
    def get_date(self, text):
        """Date starts with ^. Examples:
        
            - ^today
            - ^oct10
            - ^2010-05-01
            - ^05/01/2010
        """
        today = datetime.now().date()
        
        # Today, tomorrow
        matches = re.findall(r'\^\w+', text)
        if matches:
            day = matches[0][1:]
            if day == 'today':
                return today
            elif day == 'tomorrow':
                return today + timedelta(days=1)
                
        # Full date (Y-M-D)
        matches = re.findall(r'\^\d{4}-\d{2}-\d{2}', text)
        if matches:
            value = matches[0][1:]
            year, month, day = map(int, value.split('-'))
            date = datetime(year, month, day)
            return date
            
        # Full date (M/D/Y)
        matches = re.findall(r'\^\d{2}/\d{2}/\d{4}', text)
        if matches:
            value = matches[0][1:]
            month, day, year = map(int, value.split('-'))
            date = datetime(year, month, day)
            return date
                
        # Month and day (e.g. Jun10, dec1)
        matches = re.findall(r'\^\w+\d+', text)
        if matches:
            value = matches[0][1:].lower()
            month = self.MONTHS[value[:3]]
            day = int(value[3:])
            date = datetime(today.year, month, day)
            return date
        

class TaskInterval(models.Model):
    task = models.ForeignKey(Task)
    doer = models.ForeignKey(User)
    started = models.DateTimeField(default=datetime.now)
    duration = models.PositiveIntegerField(null=True)

    def stop(self, now=None):
        if now is None:
            now = datetime.now()
        self.duration = (now - self.started).seconds
