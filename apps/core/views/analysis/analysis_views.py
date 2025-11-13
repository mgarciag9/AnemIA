"""
Vistas para el análisis de imágenes de conjuntiva para detección de anemia.
"""

import os
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from apps.core.models import Paciente
import base64
from PIL import Image
from io import BytesIO
import traceback
import google.generativeai as genai
from decouple import config


@login_required
def analysis_view(request):
    """
    Vista principal para el análisis de imágenes de conjuntiva.
    Permite seleccionar un paciente, cargar imagen y realizar análisis.
    """
    # Obtener todos los pacientes
    pacientes = Paciente.objects.all().order_by("nombre", "apellido")

    context = {
        "pacientes": pacientes,
        "page_title": "Análisis de Imágenes",
    }

    return render(request, "core/analysis/analysis_form.html", context)


@login_required
@require_POST
def analyze_image(request):
    """
    Procesa y analiza una imagen de conjuntiva.
    Recibe la imagen recortada y el ID del paciente.
    """
    try:
        # Obtener datos del request
        paciente_id = request.POST.get("paciente_id")
        image_data = request.POST.get("image_data")  # Base64

        # Validar datos
        if not paciente_id:
            return JsonResponse(
                {"success": False, "error": "Debe seleccionar un paciente"}, status=400
            )

        if not image_data:
            return JsonResponse(
                {"success": False, "error": "No se ha cargado ninguna imagen"},
                status=400,
            )

        # Validar paciente
        try:
            paciente = Paciente.objects.get(id=paciente_id)
        except Paciente.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Paciente no encontrado"}, status=404
            )

        # Decodificar imagen base64
        try:
            # Remover el prefijo data:image/...;base64,
            if "," in image_data:
                image_data = image_data.split(",")[1]

            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))

            # Convertir a RGB si es necesario
            if image.mode != "RGB":
                image = image.convert("RGB")

        except Exception as e:
            return JsonResponse(
                {"success": False, "error": f"Error al procesar la imagen: {str(e)}"},
                status=400,
            )

        # Guardar imagen usando default_storage (funciona local y S3)
        import datetime

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analisis_{timestamp}.jpg"

        # Ruta relativa dentro de MEDIA: analysis/<paciente_id>/filename
        storage_path = f"analysis/{paciente_id}/{filename}"

        # Guardar imagen en un buffer y usar default_storage
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        # Guardar en storage (S3 o filesystem según configuración)
        default_storage.save(storage_path, ContentFile(buffer.read()))

        # Obtener URL pública (funciona para S3 y para MEDIA en local)
        try:
            image_url = default_storage.url(storage_path)
        except Exception:
            # Fallback: ruta relativa bajo /media/
            image_url = f"/media/{storage_path}"

        # Para backward-compatibilidad, establecer image_path local si storage es filesystem
        # intentaremos obtener un path en disco si existe
        try:
            if hasattr(default_storage, 'path'):
                image_path = default_storage.path(storage_path)
            else:
                image_path = storage_path
        except Exception:
            image_path = storage_path

        # Usar el detector singleton (modelo ya pre-cargado)
        try:
            from ml_models.model_loader import get_anemia_detector

            # Obtener detector (ya cargado, muy rápido)
            detector = get_anemia_detector()

            # Realizar predicción
            result = detector.predict(image_path)
        except ImportError as e:
            return JsonResponse(
                {
                    "success": False,
                    "error": "El módulo de TensorFlow no está instalado. Por favor, instala las dependencias: pip install tensorflow pillow numpy",
                },
                status=500,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Error al realizar la predicción: {str(e)}",
                },
                status=500,
            )

        # Imprimir resultados en terminal
        print("RESULTADO DEL ANÁLISIS DE ANEMIA")
        print(f"Paciente: {paciente.nombre} {paciente.apellido}")
        print(f"DNI: {paciente.dni}")
        print(f"Usuario: {request.user.email}")
        print(f"Imagen guardada en storage: {storage_path} (url: {image_url})")
        print(f"Diagnóstico: {result['diagnosis']}")
        print(
            f"Probabilidad de anemia: {result['probability']:.4f} ({result['probability']*100:.2f}%)"
        )
        print(
            f"Nivel de confianza: {result['confidence_level']} ({result['confidence']*100:.2f}%)"
        )
        print(f"Tiene anemia: {'SÍ' if result['has_anemia'] else 'NO'}")

        # Preparar respuesta
        response_data = {
            "success": True,
            "redirect_url": f"/analysis/results/{paciente.id}/?image={filename}",
            "paciente": {
                "id": paciente.id,
                "nombre": f"{paciente.nombre} {paciente.apellido}",
                "dni": paciente.dni,
            },
            "resultado": {
                "diagnostico": result["diagnosis"],
                "tiene_anemia": result["has_anemia"],
                "probabilidad": round(result["probability"], 4),
                "probabilidad_porcentaje": round(result["probability"] * 100, 2),
                "confianza": round(result["confidence"], 4),
                "confianza_porcentaje": round(result["confidence"] * 100, 2),
                "nivel_confianza": result["confidence_level"],
            },
            "imagen_guardada": filename,
            "imagen_ruta": image_url,
            "mensaje": "Análisis completado exitosamente. Redirigiendo a resultados...",
        }

        return JsonResponse(response_data)

    except Exception as e:
        error_message = str(e)
        print("\n" + "=" * 70)
        print(f"❌ ERROR EN ANÁLISIS: {error_message}")
        print("=" * 70)
        print("Traceback completo:")
        print(traceback.format_exc())
        print("=" * 70 + "\n")

        return JsonResponse(
            {
                "success": False,
                "error": f"Error al analizar la imagen: {error_message}",
            },
            status=500,
        )


@login_required
def get_patient_info(request, paciente_id):
    """
    Obtiene información de un paciente específico.
    """
    try:
        paciente = Paciente.objects.get(id=paciente_id)

        data = {
            "success": True,
            "paciente": {
                "id": paciente.id,
                "nombre": paciente.nombre,
                "apellido": paciente.apellido,
                "nombre_completo": f"{paciente.nombre} {paciente.apellido}",
                "dni": paciente.dni,
                "sexo": paciente.sexo,
                "correo": paciente.correo,
                "ciudad": paciente.ciudad,
                "direccion": paciente.direccion,
            },
        }

        return JsonResponse(data)

    except Paciente.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Paciente no encontrado"}, status=404
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def generate_diagnosis_with_gemini(
    detection_result, patient_name, confidence_percentage
):
    """
    Genera un diagnóstico médico detallado usando la API de Gemini.
    """
    try:
        # Configurar API de Gemini
        api_key = config("GEMINI_API_KEY", default="")
        if not api_key:
            return generate_fallback_diagnosis(detection_result, confidence_percentage)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Crear prompt para Gemini
        prompt = f"""
Eres un médico especialista en hematología. Basándote en el siguiente análisis de imagen conjuntival para detección de anemia, genera un informe médico detallado y profesional.

DATOS DEL ANÁLISIS:
- Paciente: {patient_name}
- Resultado de la detección: {"Anemia detectada" if detection_result['has_anemia'] else "No se detectó anemia"}
- Porcentaje de confianza: {confidence_percentage}%
- Nivel de confianza: {detection_result['confidence_level']}

Genera un informe que incluya:

1. **Observaciones Clínicas**: Descripción de la coloración conjuntival y los hallazgos visuales observados. Sé específico sobre la palidez, vascularización y apariencia general.

2. **Interpretación Preliminar**: Explica qué significan estos hallazgos en términos médicos. Indica el grado probable de anemia (leve, moderada o severa) si se detectó.

3. **Recomendaciones**: Lista de estudios de laboratorio necesarios para confirmar el diagnóstico y evaluación complementaria requerida. Incluye biometría hemática completa, niveles de ferritina y hierro sérico.

El tono debe ser profesional, médico y empático. No uses formato markdown, solo texto plano organizado con los títulos que te mencioné.
"""

        # Generar respuesta
        response = model.generate_content(prompt)
        diagnosis_text = response.text

        # Parsear la respuesta en secciones
        sections = parse_diagnosis_sections(diagnosis_text)

        return sections

    except Exception as e:
        print(f"Error al generar diagnóstico con Gemini: {str(e)}")
        return generate_fallback_diagnosis(detection_result, confidence_percentage)


def parse_diagnosis_sections(text):
    """
    Parsea el texto del diagnóstico en secciones estructuradas.
    """
    sections = {"observaciones": "", "interpretacion": "", "recomendaciones": ""}

    # Dividir por secciones
    lines = text.split("\n")
    current_section = None

    for line in lines:
        line_lower = line.lower()

        if "observaciones clínicas" in line_lower or "observaciones" in line_lower:
            current_section = "observaciones"
            continue
        elif (
            "interpretación preliminar" in line_lower or "interpretación" in line_lower
        ):
            current_section = "interpretacion"
            continue
        elif "recomendaciones" in line_lower:
            current_section = "recomendaciones"
            continue

        if current_section and line.strip():
            # Limpiar asteriscos y otros caracteres de markdown
            clean_line = line.replace("**", "").replace("*", "").strip()
            if clean_line and not clean_line.startswith("#"):
                sections[current_section] += clean_line + " "

    # Limpiar espacios extras
    for key in sections:
        sections[key] = sections[key].strip()

    return sections


def generate_fallback_diagnosis(detection_result, confidence_percentage):
    """
    Genera un diagnóstico básico cuando Gemini no está disponible.
    """
    has_anemia = detection_result["has_anemia"]
    confidence_level = detection_result["confidence_level"]

    if has_anemia:
        observaciones = (
            f"Coloración conjuntival: La mucosa conjuntival presenta una coloración "
            f"rosada pálida con notable disminución de la vascularización normal. "
            f"La conjuntiva muestra una palidez evidente en comparación con el "
            f"tono rosado-rojizo esperado en condiciones normales de oxigenación."
        )

        interpretacion = (
            f"Porcentaje de confianza: {confidence_percentage}% "
            f"Sospecha diagnóstica: Los hallazgos son compatibles con anemia de grado leve a moderado. "
            f"La palidez conjuntival observada sugiere una posible reducción en la concentración de hemoglobina, lo cual "
            f"requiere confirmación mediante estudios de laboratorio."
        )

        recomendaciones = (
            "Biometría hemática completa (hemoglobina, hematocrito, índices eritrocitarios) "
            "Evaluación de niveles de ferritina sérica y hierro "
        )
    else:
        observaciones = (
            "Coloración conjuntival: La mucosa conjuntival presenta una coloración "
            "rosada normal con adecuada vascularización. La conjuntiva muestra un "
            "tono saludable sin signos evidentes de palidez."
        )

        interpretacion = (
            f"Porcentaje de confianza: {confidence_percentage}% "
            "Los hallazgos son consistentes con una coloración conjuntival normal. "
            "No se observan signos evidentes de anemia en el examen visual de la conjuntiva. "
            "Sin embargo, esto no descarta completamente la posibilidad de anemia leve."
        )

        recomendaciones = (
            "Si existen síntomas clínicos sugestivos de anemia (fatiga, palidez generalizada, disnea), "
            "se recomienda realizar biometría hemática completa como estudio de control preventivo."
        )

    return {
        "observaciones": observaciones,
        "interpretacion": interpretacion,
        "recomendaciones": recomendaciones,
    }


@login_required
def analysis_results_view(request, paciente_id):
    """
    Vista para mostrar los resultados del análisis con diagnóstico generado por IA.
    """
    try:
        # Obtener paciente
        paciente = Paciente.objects.get(id=paciente_id)

        # Obtener nombre de imagen desde query params
        image_filename = request.GET.get("image", "")

        if not image_filename:
            return redirect("core:analysis")

        # Construir rutas
        # Usar default_storage para construir la ruta en storage
        storage_path = f"analysis/{paciente_id}/{image_filename}"

        # Obtener URL pública
        try:
            image_url = default_storage.url(storage_path)
        except Exception:
            image_url = f"/media/{storage_path}"

        # Verificar existencia usando default_storage
        try:
            exists = default_storage.exists(storage_path)
        except Exception:
            # Fallback a comprobación en disco
            exists = os.path.exists(os.path.join(settings.MEDIA_ROOT, storage_path))

        if not exists:
            return redirect("core:analysis")

        # Usar el detector singleton (modelo ya pre-cargado)
        from ml_models.model_loader import get_anemia_detector

        detector = get_anemia_detector()

        # Si tenemos un path en disco, pasarlo; en caso contrario, abrir la imagen desde storage
        try:
            # Si image_path apunta a ruta local válida (FileSystemStorage.path), usarla
            if os.path.exists(image_path):
                result = detector.predict(image_path)
            else:
                # Abrir desde storage como archivo y pasar objeto PIL al detector
                with default_storage.open(storage_path, 'rb') as f:
                    img = Image.open(f)
                    result = detector.predict(img)
        except Exception:
            # Último intento: pasar la URL (no ideal) o volver a intentar abrir desde MEDIA_ROOT
            try:
                local_try = os.path.join(settings.MEDIA_ROOT, storage_path)
                if os.path.exists(local_try):
                    result = detector.predict(local_try)
                else:
                    raise
            except Exception as e:
                raise

        # Generar diagnóstico con Gemini
        confidence_percentage = round(result["confidence"] * 100, 2)
        diagnosis = generate_diagnosis_with_gemini(
            result, f"{paciente.nombre} {paciente.apellido}", confidence_percentage
        )

        # Preparar contexto
        context = {
            "paciente": paciente,
            "imagen_url": image_url,
            "image_filename": image_filename,
            "resultado": {
                "tiene_anemia": result["has_anemia"],
                "probabilidad": round(result["probability"] * 100, 2),
                "confianza": confidence_percentage,
                "nivel_confianza": result["confidence_level"],
            },
            "diagnostico": diagnosis,
            "fecha_analisis": datetime.now().strftime("%d de %B de %Y"),
            "doctor": request.user.get_full_name() or request.user.email,
        }

        return render(request, "core/analysis/analysis_results.html", context)

    except Paciente.DoesNotExist:
        return redirect("core:analysis")
    except Exception as e:
        print(f"Error en vista de resultados: {str(e)}")
        traceback.print_exc()
        return redirect("core:analysis")


@login_required
@require_POST
def save_analysis_report(request):
    """
    Guarda el reporte de análisis en la base de datos.
    """
    try:
        from apps.core.models import ReporteAnemia
        from datetime import date

        # Obtener datos del POST
        paciente_id = request.POST.get("paciente_id")
        image_filename = request.POST.get("image_filename")
        observaciones = request.POST.get("observaciones")
        interpretacion = request.POST.get("interpretacion")
        recomendaciones = request.POST.get("recomendaciones")
        tiene_anemia = request.POST.get("tiene_anemia") == "true"
        probabilidad = float(request.POST.get("probabilidad", 0))
        confianza = float(request.POST.get("confianza", 0))
        nivel_confianza = request.POST.get("nivel_confianza", "")

        # Validar paciente
        paciente = Paciente.objects.get(id=paciente_id)

        # Determinar grado de palidez basado en el resultado
        if tiene_anemia:
            if probabilidad >= 0.8:
                grado_palidez = "Severa"
            elif probabilidad >= 0.6:
                grado_palidez = "Moderada"
            else:
                grado_palidez = "Leve"
        else:
            grado_palidez = "Ninguna"

        # Verificar si ya existe un reporte para esta imagen
        # Buscar reportes existentes para este paciente e imagen
        reportes_existentes = ReporteAnemia.objects.filter(
            paciente=paciente, imagen_conjuntiva=image_filename
        )

        # Si hay múltiples reportes duplicados, eliminar los extras y mantener solo el primero
        if reportes_existentes.count() > 1:
            reporte = reportes_existentes.first()
            # Eliminar los duplicados
            reportes_existentes.exclude(id=reporte.id).delete()
            created = False
            print(
                f"⚠️ Se encontraron y eliminaron {reportes_existentes.count() - 1} reportes duplicados"
            )
        elif reportes_existentes.exists():
            # Ya existe un reporte, actualizarlo
            reporte = reportes_existentes.first()
            created = False
        else:
            # No existe, crear uno nuevo
            reporte = ReporteAnemia()
            created = True

        # Actualizar o establecer los datos del reporte
        reporte.paciente = paciente
        reporte.fecha_analisis = date.today()
        reporte.imagen_conjuntiva = image_filename
        reporte.observaciones_clinicas = observaciones
        reporte.interpretacion_preliminar = interpretacion
        reporte.grado_palidez = grado_palidez
        reporte.sospecha_diagnostica = (
            "Anemia detectada" if tiene_anemia else "No se detectó anemia"
        )
        reporte.recomendaciones = recomendaciones
        reporte.tiene_anemia = tiene_anemia
        reporte.probabilidad = probabilidad / 100  # Convertir de porcentaje a decimal
        reporte.confianza = confianza / 100
        reporte.nivel_confianza = nivel_confianza
        reporte.creado_por = request.user
        reporte.save()

        action = "CREADO" if created else "ACTUALIZADO"
        print(f"\n✅ REPORTE {action}:")
        print(f"   ID: {reporte.id}")
        print(f"   Paciente: {paciente.nombre_completo}")
        print(f"   Fecha: {reporte.fecha_analisis}")
        print(f"   Tiene anemia: {reporte.tiene_anemia}")
        print(f"   Grado de palidez: {reporte.grado_palidez}\n")

        return JsonResponse(
            {
                "success": True,
                "message": f'Reporte {"guardado" if created else "actualizado"} exitosamente',
                "reporte_id": reporte.id,
                "created": created,
            }
        )

    except Paciente.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Paciente no encontrado"}, status=404
        )
    except Exception as e:
        print(f"Error al guardar reporte: {str(e)}")
        traceback.print_exc()
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
@require_POST
def delete_analysis_image(request):
    """
    Elimina la imagen de análisis cuando se cancela.
    """
    try:
        paciente_id = request.POST.get("paciente_id")
        image_filename = request.POST.get("image_filename")

        if not paciente_id or not image_filename:
            return JsonResponse(
                {"success": False, "error": "Datos incompletos"}, status=400
            )

        # Construir ruta de la imagen
        image_path = os.path.join(
            settings.BASE_DIR,
            "static",
            "img",
            "analysis",
            str(paciente_id),
            image_filename,
        )

        # Eliminar archivo si existe
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"✅ Imagen eliminada: {image_path}")

            return JsonResponse(
                {"success": True, "message": "Imagen eliminada exitosamente"}
            )
        else:
            return JsonResponse(
                {"success": False, "error": "Imagen no encontrada"}, status=404
            )

    except Exception as e:
        print(f"Error al eliminar imagen: {str(e)}")
        traceback.print_exc()
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
@require_POST
def delete_analysis_report(request):
    """
    Elimina un reporte de análisis de la base de datos.
    """
    try:
        from apps.core.models import ReporteAnemia

        reporte_id = request.POST.get("reporte_id")

        if not reporte_id:
            return JsonResponse(
                {"success": False, "error": "ID de reporte no proporcionado"},
                status=400,
            )

        # Obtener y eliminar el reporte
        try:
            reporte = ReporteAnemia.objects.get(id=reporte_id)

            # Verificar que el usuario tenga permiso (el que lo creó)
            if reporte.creado_por != request.user:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "No tienes permiso para eliminar este reporte",
                    },
                    status=403,
                )

            print(f"🗑️ Eliminando reporte ID: {reporte_id}")
            reporte.delete()
            print(f"✅ Reporte eliminado exitosamente")

            return JsonResponse(
                {"success": True, "message": "Reporte eliminado exitosamente"}
            )

        except ReporteAnemia.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Reporte no encontrado"}, status=404
            )

    except Exception as e:
        print(f"Error al eliminar reporte: {str(e)}")
        traceback.print_exc()
        return JsonResponse({"success": False, "error": str(e)}, status=500)
