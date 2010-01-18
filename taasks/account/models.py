from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # user = models.ForeignKey(User, unique=True)
    full_name = models.CharField(max_length=100)
    