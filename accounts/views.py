from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from .forms import SecureLoginForm

PASSWORD_MAX_AGE_DAYS = 90  # ajustable

def login_view(request):
    if request.method == "POST":
        form = SecureLoginForm(request, data=request.POST)
        if form.is_valid():
            # Rotation de session
            request.session.flush()

            user = form.get_user()
            login(request, user)

            # Option : forcer changement mot de passe si trop ancien
            last_change = getattr(user, "last_password_change", None)
            if last_change and last_change < timezone.now() - timedelta(days=PASSWORD_MAX_AGE_DAYS):
                return redirect("password_change")  # à implémenter plus tard

            return redirect("dashboard")
    else:
        form = SecureLoginForm(request)

    return render(request, "accounts/login.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")