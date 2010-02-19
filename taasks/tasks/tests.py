"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

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
            '<span class="tag">#bug</span> Fix everything '
            '<span class="due-date">^%s</span>!' \
                % today.strftime(task.DATE_FORMAT))
                
    def test_estimation(self):
        task = Task(title='Write functional tests ~3')
        self.failUnlessEqual(task.estimate, 3)
        
    def test_children(self):
        """
        o Create an iPhone app
            o Download SDK
            o Create UI
                o Make sketches
                o Write UI code
            o Write logic code
        """
        user = User(username='test')
        user.save()
        
        task = Task(title='Create an iPhone app', position=1, indent=0,
            creator=user)
        task.save()
        task_child1 = Task(title='Download SDK', position=2, indent=1,
            creator=user)
        task_child1.save()
        task_child2 = Task(title='Create UI', position=3, indent=1,
            creator=user)
        task_child2.save()
        task_child21 = Task(title='Make sketches', position=4, indent=2,
            creator=user)
        task_child21.save()
        task_child22 = Task(title='Write UI code', position=5, indent=2,
            creator=user)
        task_child22.save()
        task_child3 = Task(title='Write logic code', position=6, indent=1,
            creator=user)
        task_child3.save()
        
        self.failUnlessEqual(Task.objects.count(), 6)
        
        self.failUnlessEqual(len(task.children), 3)
        self.failUnlessEqual(task.children[0], task_child1)
        self.failUnlessEqual(task.children[1], task_child2)
        self.failUnlessEqual(task.children[2], task_child3)
        
        self.failUnlessEqual(len(task_child2.children), 2)
        self.failUnlessEqual(task_child2.children[0], task_child21)
        self.failUnlessEqual(task_child2.children[1], task_child22)


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

