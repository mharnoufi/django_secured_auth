from django.contrib.auth.backends import ModelBackend
from django.utils import timezone

class EmailBackend(ModelBackend):
    def user_can_authenticate(self, user):
        locked_until = getattr(user, "account_locked_until", None)
        if locked_until and locked_until > timezone.now():
            return False
        return super().user_can_authenticate(user)