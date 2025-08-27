from django.db import models
from datetime import timedelta
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.last_password_change = timezone.now()
        user.save(using=self._db)
        return user  # <-- important

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)      # <-- False pour un user normal
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    # on supprime totalement username, on utilise l'email comme identifiant
    username = None
    email = models.EmailField(unique=True)

    # Suivi sécurité
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    last_password_change = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # <-- attache le manager custom

    def is_locked(self):
        return bool(self.account_locked_until and self.account_locked_until > timezone.now())

    def register_failed_login(self, max_attempts: int = 5, lock_minutes: int = 15):
        """Incrémente les échecs, verrouille si seuil atteint."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            self.account_locked_until = timezone.now() + timedelta(minutes=lock_minutes)
            self.failed_login_attempts = 0
        self.save(update_fields=["failed_login_attempts", "account_locked_until"])

    def clear_failed_logins(self):
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=["failed_login_attempts", "account_locked_until"])

    def set_password(self, raw_password):
        super().set_password(raw_password)
        self.last_password_change = timezone.now()
