from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(User, primary_key=True)
    full_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    about = models.CharField(max_length=100, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    
admin.site.register(UserProfile)

def create_profile(signal, **kwargs):
    if kwargs.get('created'):
        user = kwargs.get('instance')
        profile, new = UserProfile.objects.get_or_create(user=user)

models.signals.post_save.connect(create_profile, sender=User)
