from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """User profile with various additional settings.
    """
    user = models.ForeignKey(User, primary_key=True)

    timezone = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.user.get_full_name(), self.user.email)

def create_profile(signal, **kwargs):
    if kwargs.get('created'):
        user = kwargs.get('instance')
        profile, new = UserProfile.objects.get_or_create(user=user)

models.signals.post_save.connect(create_profile, sender=User)
