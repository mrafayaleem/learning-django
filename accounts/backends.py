from django.conf import settings
from django.contrib.auth.models import check_password

from accounts.models import DubizzleUser


class EmailAuthBackend(object):
    """
    Dubizzle custom authentication backend.
    """

    def authenticate(self, email=None, password=None):
        """
        Custom authentication method to use email address.
        """
        try:
            user = DubizzleUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except DubizzleUser.DoesNotExists:
            return None

    def get_user(self, user_id):
        try:
            user = DubizzleUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except DubizzleUser.DoesNotExist:
            return None