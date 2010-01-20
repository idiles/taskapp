"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from datetime import datetime, timedelta

from django.test import TestCase

from tasks.models import Task, TaskRegexp


class TaskTest(TestCase):
    def test_html_view(self):
        tre = TaskRegexp()
        title = '#bug Fix everything ^today!'
        today = datetime.now().date()
        due_date = tre.get_date(title)
        
        task = Task(title=title,
            due_date=due_date)
            
        self.failUnlessEqual(task.html, 
            '#bug Fix everything <span class="due-date">^%s</span>!' \
                % today.strftime(task.DATE_FORMAT))


class TaskRegexpTest(TestCase):
    def test_due_date(self):
        """Test get_date() method."""
        tre = TaskRegexp()

        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        self.failUnlessEqual(tre.get_date('Do something crazy ^today'), today)
        self.failUnlessEqual(tre.get_date('Sleep well ^tomorrow'), tomorrow)

        due_date = tre.get_date('Meet friends ^Jun23 or ^Jan24.')
        self.failUnlessEqual((due_date.month, due_date.day), (6, 23))
        self.failUnlessEqual(due_date.year, today.year)

        due_date = tre.get_date('Upgrade the server ^2010-04-28')
        self.failUnlessEqual((due_date.year, due_date.month, due_date.day),
            (2010, 4, 28))
        

# __test__ = {"doctest": """
# """}

