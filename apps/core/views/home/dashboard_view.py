from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.core.models import Paciente, ReporteAnemia


class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista del dashboard principal del sistema"""

    template_name = "core/dashboard.html"
    login_url = reverse_lazy("security:login")

    def get_context_data(self, **kwargs):
        """Agregar datos adicionales al contexto"""
        context = super().get_context_data(**kwargs)

        # Contar pacientes registrados
        total_pacientes = Paciente.objects.count()

        # Contar reportes generados
        total_reportes = ReporteAnemia.objects.count()

        # Contar imágenes cargadas (reportes con imagen)
        total_imagenes = ReporteAnemia.objects.exclude(imagen_conjuntiva="").count()

        # Estadísticas del dashboard
        context["stats"] = {
            "analisis_realizados": total_reportes,
            "reportes_generados": total_reportes,
            "imagenes_cargadas": total_imagenes,
            "pacientes_registrados": total_pacientes,
        }

        # Obtener los 6 reportes más recientes
        reportes_recientes = ReporteAnemia.objects.select_related("paciente").order_by(
            "-fecha_analisis"
        )[:6]

        context["reportes_recientes"] = reportes_recientes

        return context
