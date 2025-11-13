from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión"""

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu correo",
                "required": True,
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu contraseña",
                "required": True,
            }
        ),
    )

    error_messages = {
        "invalid_login": "Correo o contraseña incorrectos. Por favor, intenta nuevamente.",
        "inactive": "Esta cuenta está inactiva.",
    }


class RegisterForm(forms.ModelForm):
    """Formulario de registro de nuevos usuarios"""

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu contraseña",
                "required": True,
            }
        ),
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirma tu contraseña",
                "required": True,
            }
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingresa tu nombre",
                    "required": True,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingresa tu apellido",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingresa tu correo electrónico",
                    "required": True,
                }
            ),
        }
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
        }

    def clean_email(self):
        """Validar que el email no exista"""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_password_confirm(self):
        """Validar que las contraseñas coincidan"""
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")

        return password_confirm

    def clean_password(self):
        """Validar la contraseña"""
        password = self.cleaned_data.get("password")

        if password and len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        return password

    def save(self, commit=True):
        """Guardar el usuario con la contraseña encriptada"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True

        if commit:
            user.save()

        return user


class PasswordResetRequestForm(PasswordResetForm):
    """Formulario para solicitar restablecimiento de contraseña"""

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu correo electrónico",
                "required": True,
            }
        ),
    )

    def clean_email(self):
        """Validar que el email exista en el sistema"""
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise ValidationError(
                "No existe una cuenta asociada a este correo electrónico."
            )
        return email


class SetNewPasswordForm(SetPasswordForm):
    """Formulario para establecer nueva contraseña"""

    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu nueva contraseña",
                "required": True,
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirma tu nueva contraseña",
                "required": True,
            }
        ),
    )

    def clean_new_password1(self):
        """Validar la nueva contraseña"""
        password = self.cleaned_data.get("new_password1")

        if password and len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        return password
