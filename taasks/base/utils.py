from django.contrib.auth.backends import ModelBackend as DjangoModelBackend
from django.contrib.auth.models import User

from models import ExtUser


class ModelBackend(DjangoModelBackend):
    """Authenticates against base.models.ExtUser.
    """

    def authenticate(self, username=None, password=None):
        # Try ExtUser first
        try:
            user = ExtUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except ExtUser.DoesNotExist:
            pass

        # Fallback to User (special users, like admin)
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

        # Sorry, no go
        return None

    def get_user(self, user_id):
        # Try ExtUser first
        try:
            return ExtUser.objects.get(pk=user_id)
        except ExtUser.DoesNotExist:
            pass

        # Fallback to User
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass

        # We don't know you
        return None
