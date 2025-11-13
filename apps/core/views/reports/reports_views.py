from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from apps.core.models import ReporteAnemia
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO
import os


@login_required
def reports_list_view(request):
    """Vista para listar todos los reportes de anemia"""

    # Obtener parámetro de búsqueda
    search_query = request.GET.get("search", "").strip()

    # Obtener todos los reportes del doctor actual
    reportes = ReporteAnemia.objects.filter(creado_por=request.user).select_related(
        "paciente", "creado_por"
    )

    # Aplicar filtro de búsqueda si existe
    if search_query:
        reportes = reportes.filter(
            Q(paciente__nombre__icontains=search_query)
            | Q(paciente__apellido__icontains=search_query)
            | Q(paciente__correo__icontains=search_query)
            | Q(paciente__id__icontains=search_query)
        )

    # Ordenar por fecha más reciente
    reportes = reportes.order_by("-fecha_analisis", "-creado_en")

    # Paginación
    paginator = Paginator(reportes, 6)  # 6 reportes por página (2x3 grid)
    page = request.GET.get("page", 1)

    try:
        reportes_pagina = paginator.page(page)
    except PageNotAnInteger:
        reportes_pagina = paginator.page(1)
    except EmptyPage:
        reportes_pagina = paginator.page(paginator.num_pages)

    context = {
        "reportes": reportes_pagina,
        "search_query": search_query,
        "total_reportes": paginator.count,
    }

    return render(request, "core/reports/reports_list.html", context)


@login_required
def report_detail_view(request, report_id):
    """Vista para ver el detalle completo de un reporte"""

    reporte = get_object_or_404(ReporteAnemia, id=report_id, creado_por=request.user)

    context = {
        "reporte": reporte,
    }

    return render(request, "core/reports/report_detail.html", context)


@login_required
def delete_report(request, report_id):
    """Vista para eliminar un reporte"""

    if request.method == "POST":
        reporte = get_object_or_404(
            ReporteAnemia, id=report_id, creado_por=request.user
        )

        paciente_nombre = reporte.paciente.nombre_completo
        reporte.delete()

        messages.success(
            request, f"Reporte de {paciente_nombre} eliminado exitosamente."
        )

        return redirect("core:reports_list")

    return redirect("core:reports_list")


def _generate_pdf_content(reporte, request_user):
    """
    Función auxiliar para generar el contenido del PDF
    Retorna un BytesIO con el PDF generado
    """
    # Crear buffer en memoria
    buffer = BytesIO()

    # Crear el PDF en el buffer
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Contenedor para los elementos del PDF
    story = []

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#2C5F7B"),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#7fa8b5"),
        spaceAfter=12,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )

    # Estilo para texto normal
    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName="Helvetica",
    )

    # Título principal
    story.append(Paragraph("REPORTE DE DETECCIÓN DE ANEMIA", title_style))
    story.append(Paragraph("Análisis Conjuntival", subtitle_style))
    story.append(Spacer(1, 0.2 * inch))

    # Información del paciente
    story.append(Paragraph("INFORMACIÓN DEL PACIENTE", subtitle_style))

    patient_data = [
        ["Nombre:", f"{reporte.paciente.nombre} {reporte.paciente.apellido}"],
        ["DNI:", reporte.paciente.dni],
        ["Correo:", reporte.paciente.correo],
        ["Fecha de análisis:", reporte.fecha_analisis.strftime("%d de %B de %Y")],
    ]

    patient_table = Table(patient_data, colWidths=[1.5 * inch, 4 * inch])
    patient_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#2C5F7B")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(patient_table)
    story.append(Spacer(1, 0.3 * inch))

    # Resultado del análisis
    story.append(Paragraph("RESULTADOS DEL ANÁLISIS", subtitle_style))

    # Diagnóstico principal
    diagnostico_color = (
        colors.HexColor("#d32f2f")
        if reporte.tiene_anemia
        else colors.HexColor("#388e3c")
    )
    diagnostico_text = (
        "ANEMIA DETECTADA" if reporte.tiene_anemia else "NO SE DETECTÓ ANEMIA"
    )

    result_data = [
        ["Diagnóstico:", diagnostico_text],
        ["Grado de Palidez:", reporte.grado_palidez.title()],
        ["Probabilidad:", f"{reporte.probabilidad:.1f}%"],
        ["Nivel de Confianza:", reporte.nivel_confianza],
    ]

    result_table = Table(result_data, colWidths=[1.5 * inch, 4 * inch])
    result_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#2C5F7B")),
                ("TEXTCOLOR", (1, 0), (1, 0), diagnostico_color),
                ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(result_table)
    story.append(Spacer(1, 0.2 * inch))

    # Imagen de la conjuntiva (si existe)
    image_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "img",
        "analysis",
        str(reporte.paciente.id),
        reporte.imagen_conjuntiva,
    )

    if os.path.exists(image_path):
        try:
            img = Image(image_path, width=3 * inch, height=3 * inch)
            story.append(Paragraph("IMAGEN ANALIZADA", subtitle_style))
            story.append(img)
            story.append(Spacer(1, 0.2 * inch))
        except Exception as e:
            print(f"Error al cargar imagen en PDF: {e}")

    # Observaciones clínicas
    story.append(Paragraph("OBSERVACIONES CLÍNICAS", subtitle_style))
    story.append(Paragraph(reporte.observaciones_clinicas, normal_style))
    story.append(Spacer(1, 0.1 * inch))

    # Interpretación preliminar
    story.append(Paragraph("INTERPRETACIÓN PRELIMINAR", subtitle_style))
    story.append(
        Paragraph(
            f"<b>Grado de palidez conjuntival:</b> {reporte.grado_palidez.title()}",
            normal_style,
        )
    )
    story.append(
        Paragraph(
            f"<b>Sospecha diagnóstica:</b> {reporte.sospecha_diagnostica}", normal_style
        )
    )
    story.append(Paragraph(reporte.interpretacion_preliminar, normal_style))
    story.append(Spacer(1, 0.1 * inch))

    # Recomendaciones
    story.append(Paragraph("RECOMENDACIONES", subtitle_style))
    story.append(Paragraph(reporte.recomendaciones, normal_style))
    story.append(Spacer(1, 0.3 * inch))

    # Pie de página
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.gray,
        alignment=TA_CENTER,
        fontName="Helvetica-Oblique",
    )

    story.append(Spacer(1, 0.5 * inch))
    story.append(
        Paragraph("_______________________________________________", footer_style)
    )
    story.append(
        Paragraph(
            f"Reporte generado por: {request_user.get_full_name() or request_user.username}",
            footer_style,
        )
    )
    story.append(Paragraph("Sistema de Detección de Anemia", footer_style))
    story.append(
        Paragraph(
            f"Fecha de generación: {reporte.creado_en.strftime('%d de %B de %Y - %H:%M')}",
            footer_style,
        )
    )

    # Generar el PDF
    doc.build(story)

    # Mover el puntero al inicio del buffer
    buffer.seek(0)

    return buffer


@login_required
def send_report_email(request, report_id):
    """Vista para enviar reporte por email con PDF adjunto"""

    if request.method == "POST":
        reporte = get_object_or_404(
            ReporteAnemia, id=report_id, creado_por=request.user
        )

        try:
            # Generar PDF
            pdf_buffer = _generate_pdf_content(reporte, request.user)
            pdf_filename = f"Reporte_Anemia_{reporte.paciente.nombre}_{reporte.paciente.apellido}_{reporte.fecha_analisis.strftime('%Y%m%d')}.pdf"

            # Preparar el asunto del correo
            subject = (
                f"Reporte de Detección de Anemia - {reporte.paciente.nombre_completo}"
            )

            # Preparar el mensaje
            message = f"""Estimado/a {reporte.paciente.nombre_completo},

Le enviamos adjunto el reporte de su análisis de detección de anemia realizado el {reporte.fecha_analisis.strftime('%d de %B de %Y')}.

RESUMEN DE RESULTADOS:
----------------------

Diagnóstico: {'ANEMIA DETECTADA' if reporte.tiene_anemia else 'NO SE DETECTÓ ANEMIA'}
Grado de Palidez: {reporte.grado_palidez.title()}
Probabilidad: {reporte.probabilidad:.1f}%
Nivel de Confianza: {reporte.nivel_confianza}

Por favor, revise el documento PDF adjunto para ver el reporte completo con todas las observaciones, interpretación y recomendaciones.

---
Este es un reporte automático generado por el Sistema de Detección de Anemia.
Para más información, consulte con su médico tratante.

Atentamente,
{request.user.get_full_name() or request.user.username}
Sistema de Detección de Anemia
"""

            # Crear el email con adjunto
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=getattr(
                    settings, "DEFAULT_FROM_EMAIL", "noreply@anemia-detection.com"
                ),
                to=[reporte.paciente.correo],
            )

            # Adjuntar el PDF
            email.attach(pdf_filename, pdf_buffer.read(), "application/pdf")

            # Enviar el correo
            email.send(fail_silently=False)

            messages.success(
                request,
                f"Reporte enviado exitosamente por email a {reporte.paciente.correo} con PDF adjunto",
            )

        except Exception as e:
            messages.error(
                request,
                f"Error al enviar el correo: {str(e)}. Verifique la configuración de email.",
            )

        # Redirigir de vuelta al detalle del reporte
        return redirect("core:report_detail", report_id=report_id)

    return redirect("core:reports_list")


@login_required
def generate_report_pdf(request, report_id):
    """Vista para generar y descargar PDF del reporte"""

    reporte = get_object_or_404(ReporteAnemia, id=report_id, creado_por=request.user)

    # Generar PDF usando la función auxiliar
    pdf_buffer = _generate_pdf_content(reporte, request.user)

    # Crear respuesta HTTP con PDF
    response = HttpResponse(pdf_buffer.read(), content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="Reporte_Anemia_{reporte.paciente.nombre}_{reporte.paciente.apellido}_{reporte.fecha_analisis.strftime("%Y%m%d")}.pdf"'
    )

    return response
