from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    
    
# def create_profile(signal, **kwargs):
#     if kwargs.get('created'):
#         user = kwargs.get('instance')
#         profile, new = UserProfile.objects.get_or_create(user=user)
# 
# models.signals.post_save.connect(create_profile, sender=User)