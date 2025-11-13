from django.db import models
from apps.security.models import CustomUser


class Paciente(models.Model):

    class SexoChoices(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMENINO = "F", "Femenino"
        OTRO = "O", "Otro"

    id = models.CharField(max_length=20, primary_key=True, verbose_name="ID Paciente")

    doctor_responsable = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="pacientes",
        verbose_name="Doctor Responsable",
    )

    nombre = models.CharField(max_length=100, verbose_name="Nombre(s)")
    apellido = models.CharField(max_length=100, verbose_name="Apellido(s)")
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    sexo = models.CharField(
        max_length=1, choices=SexoChoices.choices, verbose_name="Sexo"
    )
    ciudad = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Ciudad"
    )
    direccion = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Dirección"
    )
    foto_perfil = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Foto de Perfil"
    )

    fecha_registro = models.DateField(
        auto_now_add=True, verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["-fecha_registro"]

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return self.nombre_completo


class ReporteAnemia(models.Model):

    class GradoPalidezChoices(models.TextChoices):
        LEVE = "Leve", "Leve"
        MODERADA = "Moderada", "Moderada"
        SEVERA = "Severa", "Severa"
        NINGUNA = "Ninguna", "Ninguna"

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="reportes",
        verbose_name="Paciente",
    )

    fecha_analisis = models.DateField(verbose_name="Fecha de Análisis")

    imagen_conjuntiva = models.CharField(
        max_length=255, verbose_name="Imagen Conjuntiva"
    )

    observaciones_clinicas = models.TextField(verbose_name="Observaciones Clínicas")
    interpretacion_preliminar = models.TextField(
        verbose_name="Interpretación Preliminar"
    )
    grado_palidez = models.CharField(
        max_length=20,
        choices=GradoPalidezChoices.choices,
        verbose_name="Grado de Palidez",
    )
    sospecha_diagnostica = models.TextField(verbose_name="Sospecha Diagnóstica")
    recomendaciones = models.TextField(verbose_name="Recomendaciones")

    # Nuevos campos para resultados de ML
    tiene_anemia = models.BooleanField(default=False, verbose_name="Tiene Anemia")
    probabilidad = models.FloatField(verbose_name="Probabilidad")
    confianza = models.FloatField(verbose_name="Confianza")
    nivel_confianza = models.CharField(max_length=50, verbose_name="Nivel de Confianza")

    creado_por = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="Creado Por"
    )
    creado_en = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación"
    )

    class Meta:
        verbose_name = "Reporte de Anemia"
        verbose_name_plural = "Reportes de Anemia"
        ordering = ["-fecha_analisis"]

    def get_imagen_url(self):
        """Retorna la URL completa de la imagen conjuntiva"""
        if self.imagen_conjuntiva:
            return f"/static/img/analysis/{self.paciente.id}/{self.imagen_conjuntiva}"
        return None

    def __str__(self):
        return f"Reporte de {self.paciente.nombre_completo} - {self.fecha_analisis}"
