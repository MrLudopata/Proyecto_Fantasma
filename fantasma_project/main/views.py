# main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django import forms

# Tu LogoutView custom sigue igual
class LogoutViewAllowGet(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# Página principal protegida
@login_required
def home(request):
    return render(request, 'main/home.html')


# ✅ Formulario personalizado de registro
class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=12,
        min_length=8,
        help_text="Debe tener entre 8 y 12 caracteres.",
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Mínimo 6, máximo 16 caracteres. Debe contener mayúsculas, minúsculas y números.",
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Ingrese la misma contraseña.",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    # Validación extra para la contraseña
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 6 or len(password) > 16:
            raise forms.ValidationError("La contraseña debe tener entre 6 y 16 caracteres.")
        if not any(c.isupper() for c in password):
            raise forms.ValidationError("Debe contener al menos una letra mayúscula.")
        if not any(c.islower() for c in password):
            raise forms.ValidationError("Debe contener al menos una letra minúscula.")
        if not any(c.isdigit() for c in password):
            raise forms.ValidationError("Debe contener al menos un número.")
        return password


def register(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # NO hagas login(request, user)
            return redirect("register_success")
    else:
        form = CustomRegisterForm()
    return render(request, "main/register.html", {"form": form})

def register_success(request):
    return render(request, "main/register_success.html")
