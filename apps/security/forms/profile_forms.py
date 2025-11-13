from django import forms
from apps.security.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm


class ProfileUpdateForm(forms.ModelForm):
    """Formulario para actualizar información del perfil del usuario"""

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "city",
            "national_id",
            "gender",
            "profile_photo",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese su nombre",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese sus apellidos",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "correo@ejemplo.com",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese su teléfono",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese su dirección",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese su ciudad",
                }
            ),
            "national_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese su DNI",
                }
            ),
            "gender": forms.Select(
                attrs={"class": "form-control"},
                choices=[
                    ("", "Seleccione sexo"),
                    ("Masculino", "Masculino"),
                    ("Femenino", "Femenino"),
                    ("Otro", "Otro"),
                ],
            ),
            "profile_photo": forms.FileInput(
                attrs={
                    "class": "file-input",
                    "accept": "image/*",
                    "id": "foto_perfil",
                }
            ),
        }
        labels = {
            "first_name": "Nombre(s)",
            "last_name": "Apellido(s)",
            "email": "Correo Electrónico",
            "phone_number": "Teléfono",
            "address": "Dirección",
            "city": "Ciudad",
            "national_id": "DNI",
            "gender": "Sexo",
            "profile_photo": "Foto de Perfil",
        }

    def clean_email(self):
        """Validar que el email no esté siendo usado por otro usuario"""
        email = self.cleaned_data.get("email")
        user_id = self.instance.id

        # Verificar si existe otro usuario con el mismo email
        if CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError(
                "Este correo electrónico ya está siendo utilizado por otro usuario."
            )

        return email

    def clean_phone_number(self):
        """Validar formato de teléfono"""
        phone = self.cleaned_data.get("phone_number")
        if phone and not phone.replace("+", "").replace(" ", "").isdigit():
            raise forms.ValidationError(
                "El número de teléfono solo debe contener números."
            )
        return phone


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulario personalizado para cambio de contraseña"""

    old_password = forms.CharField(
        label="Contraseña Actual",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese su contraseña actual",
            }
        ),
    )

    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese nueva contraseña (mínimo 8 caracteres)",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme la nueva contraseña",
            }
        ),
    )

    def clean_new_password1(self):
        """Validar longitud mínima de contraseña"""
        password = self.cleaned_data.get("new_password1")
        if password and len(password) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        return password
