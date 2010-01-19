import os

from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

class UserProfile(models.Model):
    
    def make_photo_upload_path(instance, filename):
        import pdb; pdb.set_trace()
        ext = os.splitpath(filename)[1]
        path = 'photos/%s%s' % (instance.user.id, ext)
        print path
        return path
        
    
    user = models.ForeignKey(User, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    about = models.CharField(max_length=100, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to=make_photo_upload_path, null=True)
    
admin.site.register(UserProfile)

def create_profile(signal, **kwargs):
    if kwargs.get('created'):
        user = kwargs.get('instance')
        profile, new = UserProfile.objects.get_or_create(user=user)

models.signals.post_save.connect(create_profile, sender=User)
