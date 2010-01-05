from django.db import models
from django.contrib.auth.models import User

class ExtUser(User):
    """Extended user with various additional settings.
    """
    timezone = models.CharField(max_length=50, null=True)
