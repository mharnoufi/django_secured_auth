from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.dispatch import receiver

User = get_user_model()

@receiver(user_login_failed)
def on_login_failed(sender, credentials, **kwargs):
    email = credentials.get("username") or credentials.get("email")
    if not email:
        return
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return
    user.register_failed_login()  # seuil=5, verrouillage=15 min par défaut

@receiver(user_logged_in)
def on_logged_in(sender, user, request, **kwargs):
    user.clear_failed_logins()