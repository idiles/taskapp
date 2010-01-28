"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User

# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.failUnlessEqual(1 + 1, 2)
        
class UserConnectionTest(TestCase):
    def setUp(self):
        self.john = User(username='john')
        self.john.save()
        
        self.pete = User(username='pete')
        self.pete.save()
        
        self.john_profile = self.john.get_profile()
        self.pete_profile = self.pete.get_profile()
        
    def test_new_connection(self):
        connections = self.john_profile.get_connections()
        self.failUnlessEqual(len(connections), 0)
        
        self.john_profile.add_connection(self.pete)
        connections = self.john_profile.get_connections()
        self.failUnlessEqual(len(connections), 1)
        self.failUnlessEqual(self.john_profile.has_connection(self.pete), True)
        
        try:
            self.pete_profile.add_connection(self.john)
            self.fail('Exception should be raised when creating existing connection')
        except ValueError:
            pass
        
    def test_connection_removal(self):
        connections = self.john_profile.get_connections()
        self.failUnlessEqual(len(connections), 0)
        
        self.john_profile.add_connection(self.pete)
        connections = self.john_profile.get_connections()
        self.failUnlessEqual(len(connections), 1)
        
        self.john_profile.remove_connection(self.pete)
        connections = self.john_profile.get_connections()
        self.failUnlessEqual(len(connections), 0)
        
        try:
            self.pete_profile.remove_connection(self.john)
            self.fail('Exception should be raised when removing non-existing connection')
        except ValueError:
            pass
        

# __test__ = {"doctest": """
# Another way to test that 1 + 1 is equal to 2.
# 
# >>> 1 + 1 == 2
# True
# """}

