import os

from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

class UserProfile(models.Model):
    
    def make_picture_upload_path(instance, filename):
        ext = os.path.splitext(filename)[1]
        path = 'pictures/%s%s' % (instance.user.id, ext)
        return path
        
    user = models.ForeignKey(User, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    about = models.CharField(max_length=100, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    picture = models.ImageField(upload_to=make_picture_upload_path, null=True)
    
    def get_picture_url(self, size):
        if self.picture:
            url = self.picture.url
            parts = os.path.splitext(url)
            url = '%s%s%s' % (parts[0], size, parts[1])
            return url
        else:
            return '/img/avatar-%s.jpg' % size
    
    @property
    def small_picture_url(self):
        return self.get_picture_url('s')
        
    @property
    def medium_picture_url(self):
        return self.get_picture_url('m')
    
admin.site.register(UserProfile)

def create_profile(signal, **kwargs):
    if kwargs.get('created'):
        user = kwargs.get('instance')
        profile, new = UserProfile.objects.get_or_create(user=user)

models.signals.post_save.connect(create_profile, sender=User)
