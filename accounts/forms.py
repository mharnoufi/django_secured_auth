from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

GENERIC_ERROR = "Email ou mot de passe incorrect."

class SecureLoginForm(AuthenticationForm):
    """
    - Vérifie si le compte est verrouillé
    - Compte les échecs et lock 30 min après 5 échecs sur 30 min
    - Message d'erreur générique (ne révèle pas si l'email existe)
    """

    def clean(self):
        cleaned_data = super().clean()  # conserve la validation de base (CSRF, etc.)
        email = self.cleaned_data.get("username")  # AuthenticationForm utilise username => ici ton USERNAME_FIELD=email
        password = self.cleaned_data.get("password")

        # On tente de retrouver l'utilisateur, mais on ne révélera pas s'il existe
        user = None
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = None

        # 1) Compte verrouillé ?
        if user and getattr(user, "account_locked_until", None):
            if user.account_locked_until > timezone.now():
                raise forms.ValidationError(GENERIC_ERROR, code="invalid_login")
            else:
                # lock expiré : on nettoie
                user.clear_failed_logins()

        # 2) Authentification
        # NB: selon ton backend, c'est bien authenticate(request, email=..., password=...)
        # mais on garde un fallback avec username=email pour compat.
        authed = authenticate(self.request, email=email, password=password)
        if authed is None:
            authed = authenticate(self.request, username=email, password=password)

        # 3) Gestion des échecs
        if authed is None:
            if user:
                user.register_failed_login(max_attempts=5, lock_minutes=30, window_minutes=30)
            raise forms.ValidationError(GENERIC_ERROR, code="invalid_login")

        # 4) Succès : reset compteur d'échecs
        if user:
            user.clear_failed_logins()

        # Confiance finale
        self.user_cache = authed
        return cleaned_data
