from django.urls import path
from apps.core.views.home import DashboardView
from apps.core.views.patients import (
    PatientListView,
    PatientDetailView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
)
from apps.core.views.analysis import (
    analysis_view,
    analyze_image,
    get_patient_info,
    analysis_results_view,
    save_analysis_report,
    delete_analysis_image,
    delete_analysis_report,
)
from apps.core.views.reports import (
    reports_list_view,
    report_detail_view,
    delete_report,
    send_report_email,
    generate_report_pdf,
)

app_name = "core"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    # URLs de Pacientes
    path("pacientes/", PatientListView.as_view(), name="patient_list"),
    path("pacientes/crear/", PatientCreateView.as_view(), name="patient_create"),
    path(
        "pacientes/<str:patient_id>/",
        PatientDetailView.as_view(),
        name="patient_detail",
    ),
    path(
        "pacientes/<str:patient_id>/editar/",
        PatientUpdateView.as_view(),
        name="patient_update",
    ),
    path(
        "pacientes/<str:patient_id>/eliminar/",
        PatientDeleteView.as_view(),
        name="patient_delete",
    ),
    # URLs de Análisis de Imágenes
    path("analysis/", analysis_view, name="analysis"),
    path("analysis/analyze/", analyze_image, name="analyze_image"),
    path("analysis/patient/<int:paciente_id>/", get_patient_info, name="patient_info"),
    path(
        "analysis/results/<str:paciente_id>/",
        analysis_results_view,
        name="analysis_results",
    ),
    path("analysis/save/", save_analysis_report, name="save_analysis_report"),
    path("analysis/delete-image/", delete_analysis_image, name="delete_analysis_image"),
    path(
        "analysis/delete-report/", delete_analysis_report, name="delete_analysis_report"
    ),
    # URLs de Reportes
    path("reportes/", reports_list_view, name="reports_list"),
    path("reportes/<int:report_id>/", report_detail_view, name="report_detail"),
    path("reportes/<int:report_id>/eliminar/", delete_report, name="delete_report"),
    path(
        "reportes/<int:report_id>/enviar-email/",
        send_report_email,
        name="send_report_email",
    ),
    path(
        "reportes/<int:report_id>/generar-pdf/",
        generate_report_pdf,
        name="generate_report_pdf",
    ),
]
