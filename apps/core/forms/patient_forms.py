from django import forms
from django.core.exceptions import ValidationError
from apps.core.models import Paciente
from apps.core.validators import validate_ecuadorian_cedula


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'sexo', 'ciudad', 'correo', 'dni', 'direccion', 'foto_perfil']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu correo electrónico'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dni'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'style': 'display: none;',
                'id': 'foto-upload'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sexo'].empty_label = 'Sexo'
        self.fields['ciudad'].required = False
        self.fields['direccion'].required = False
        self.fields['foto_perfil'].required = False

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni:
            return dni
        try:
            validate_ecuadorian_cedula(dni)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return dni
