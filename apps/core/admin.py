from django.contrib import admin
from apps.core.models import Paciente, ReporteAnemia


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_completo', 'dni', 'correo', 'sexo', 'doctor_responsable', 'fecha_registro']
    list_filter = ['sexo', 'ciudad', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'dni', 'correo']
    readonly_fields = ['fecha_registro']


@admin.register(ReporteAnemia)
class ReporteAnemiaAdmin(admin.ModelAdmin):
    list_display = ['id', 'paciente', 'fecha_analisis', 'grado_palidez', 'creado_por', 'creado_en']
    list_filter = ['grado_palidez', 'fecha_analisis', 'creado_en']
    search_fields = ['paciente__nombre', 'paciente__apellido', 'paciente__dni']
    readonly_fields = ['creado_en']
