from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from emailusernames.utils import get_user


class ForceAuthBackend(ModelBackend):

    """Allow users to log in with their email address"""

    def authenticate(self, email=None, password=None, force=False):
        if force is False:
            return None
        
        try:
            user = get_user(email)
            user.backend = "%s.%s" % (self.__module__, self.__class__.__name__)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
