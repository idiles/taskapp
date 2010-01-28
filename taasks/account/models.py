import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Max, Sum, Q
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
    
    def __unicode__(self):
        return '%s (%s)' % (self.user.username, self.name)
    
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
        
    def get_connections(self):
        connections = []
        for c in UserConnection.objects.filter(
                Q(user1=self.user) | Q(user2=self.user)):
            if c.user1 == self.user:
                profile = c.user2.get_profile()
            else:
                profile = c.user1.get_profile()
            if c.confirmed:
                profile.connection_complete = True
            else:
                profile.connection_waiting = True
                if c.iniciator != self.user:
                    profile.connection_can_confirm = True
            connections.append(profile)
        return connections
        
    def add_connection(self, user):
        if UserConnection.objects.filter(
                Q(user1=self.user, user2=user) | Q(user1=user, 
                    user2=self.user)).count() == 0:
            connection = UserConnection(user1=self.user, user2=user,
                iniciator=self.user)
            connection.save()
            return connection
        else:
            raise ValueError('Connection between %s and %s already exists' \
                % (self.user, user))
                
    def remove_connection(self, user):
        connections = UserConnection.objects.filter(
            Q(user1=self.user, user2=user) | Q(user1=user, user2=self.user))
                
        if connections.count() == 1:
            connections[0].delete()
        else:
            raise ValueError('%d connections exist between %s and %s' \
                % (connections.count(), self.user, user))
                
    def has_connection(self, user):
        return UserConnection.objects.filter(
            Q(user1=self.user, user2=user) | Q(user1=user, user2=self.user)
            ).count() == 1
            
    # def has_waiting_connection(self, user):
    #     return UserConnection.objects.filter(
    #         Q(user1=self.user, user2=self.user) | Q(user1=user, user2=self.user), 
    #             confirmed=False).count() == 1
    
    def confirm_connection(self, user):
        connection = UserConnection.objects.filter(
            Q(user1=self.user) | Q(user2=self.user), confirmed=False,
                iniciator=user)[0]
        connection.confirmed = True
        connection.save()
        
    
admin.site.register(UserProfile)

def create_profile(signal, **kwargs):
    if kwargs.get('created'):
        user = kwargs.get('instance')
        profile, new = UserProfile.objects.get_or_create(user=user)

models.signals.post_save.connect(create_profile, sender=User)


class UserConnection(models.Model):
    user1 = models.ForeignKey(User, related_name='connection_user1')
    user2 = models.ForeignKey(User, related_name='connection_user2')
    iniciator = models.ForeignKey(User, related_name='connection_iniciator')
    confirmed = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(default=datetime.now)
    