"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from datetime import datetime, timedelta

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)
        

__test__ = {"doctest": """

Test task text regular expressions.

>>> from tasks.models import TaskRegexp
>>> tre = TaskRegexp()

>>> today = datetime.now().date()
>>> tomorrow = today + timedelta(days=1)
>>> tre.get_date('Do something crazy ^today') == today
True
>>> tre.get_date('Sleep well ^tomorrow') == tomorrow
True

>>> due_date = tre.get_date('Meet friends ^Jun23 or ^Jan24.')
>>> due_date.month, due_date.day
(6, 23)
>>> due_date.year == today.year
True

>>> due_date = tre.get_date('Upgrade the server ^2010-04-28')
>>> due_date.year, due_date.month, due_date.day
(2010, 4, 28)

"""}

