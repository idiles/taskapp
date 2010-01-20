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
    due_date = models.DateField(blank=True, null=True)
    
    DATE_FORMAT = '%Y-%m-%d'

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
    def html(self):
        """HTML view."""
        tre = TaskRegexp()
        title = self.title
        if self.due_date:
            due_date = self.due_date.strftime(self.DATE_FORMAT)
            
            for regexp in [tre.DATE_FULL_ISO_RE, tre.DATE_FULL_RE, 
                    tre.DATE_MONTH_DAY_RE, tre.DATE_DAY_RE]:
                if re.findall(regexp, title):
                    title = re.sub(regexp, 
                        '<span class="due-date">^%s</span>' % due_date, 
                        title)
                    break
             
        # Tags       
        TAG_RE = r'\#\w+\d*'
        matches = re.findall(TAG_RE, title)
        for m in matches:
            tag = m[1:]
            title = title.replace(m, '<span class="tag">#%s</span>' % tag)
            
        # Estimate
        ESTIMATE_RE = r'~\d+'
        matches = re.findall(ESTIMATE_RE, title)
        if matches:
            estimate = matches[0][1:]
            title = title.replace(matches[0], 
                '<span class="estimate">~%s</span>' % estimate)

        # Users
        USER_RE = r'@\w+\d*'
        matches = re.findall(USER_RE, title)
        if matches:
            username = matches[0][1:]
            css_class = ''
            if User.objects.filter(username=username).count() == 0:
                css_class = ' invalid-data'
                
            title = title.replace(matches[0], 
                '<span class="responsible-user%(css)s">@%(u)s</span>' \
                    % dict(u=username, css=css_class))

        return title
        
    @property
    def tags(self):
        """Exctract all tags from the task title."""
        TAG_RE = r'\#\w+\d*'
        matches = re.findall(TAG_RE, self.title)
        tags = []
        for m in matches:
            tags.append(m[1:])
        return tags
        
    @property
    def estimate(self):
        """Exctract estimate in hours from the task title."""
        ESTIMATE_RE = r'~\d+'
        matches = re.findall(ESTIMATE_RE, self.title)
        if matches:
            estimate = int(matches[0][1:])
            return estimate
            
            
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
    
    DATE_DAY_RE = r'\^\w+'
    DATE_FULL_ISO_RE = r'\^\d{4}-\d{2}-\d{2}'
    DATE_FULL_RE = r'\^\d{2}/\d{2}/\d{4}'
    DATE_MONTH_DAY_RE = r'\^\w+\d+'
    
    def get_date(self, text):
        """Date starts with ^. Examples:
        
            - ^today, ^tomorrow
            - ^oct10
            - ^2010-05-01
            - ^05/01/2010
        """
        today = datetime.now().date()
        
        # Today, tomorrow
        matches = re.findall(self.DATE_DAY_RE, text)
        if matches:
            day = matches[0][1:]
            if day == 'today':
                return today
            elif day == 'tomorrow':
                date = today + timedelta(days=1)
                return date
                
        # Full date (Y-M-D)
        matches = re.findall(self.DATE_FULL_ISO_RE, text)
        if matches:
            value = matches[0][1:]
            year, month, day = map(int, value.split('-'))
            date = datetime(year, month, day)
            return date
            
        # Full date (M/D/Y)
        matches = re.findall(self.DATE_FULL_RE, text)
        if matches:
            value = matches[0][1:]
            month, day, year = map(int, value.split('-'))
            date = datetime(year, month, day)
            return date
                
        # Month and day (e.g. Jun10, dec1)
        matches = re.findall(self.DATE_MONTH_DAY_RE, text)
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
