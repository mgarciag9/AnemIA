"""
Script para verificar las rutas de las imágenes en los reportes
"""

import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anemia_project.settings")
django.setup()

from apps.core.models import ReporteAnemia

print("=" * 80)
print("VERIFICACIÓN DE RUTAS DE IMÁGENES EN REPORTES")
print("=" * 80)

reportes = ReporteAnemia.objects.all()[:5]  # Solo los primeros 5

if not reportes:
    print("\n❌ No hay reportes en la base de datos")
else:
    for i, reporte in enumerate(reportes, 1):
        print(f"\n{i}. Reporte ID: {reporte.id}")
        print(
            f"   Paciente: {reporte.paciente.nombre_completo} (ID: {reporte.paciente.id})"
        )
        print(f"   Imagen guardada: {reporte.imagen_conjuntiva}")
        print(f"   URL construida: {reporte.get_imagen_url()}")

        # Verificar si el archivo existe
        if reporte.imagen_conjuntiva:
            full_path = os.path.join(
                "static",
                "img",
                "analysis",
                str(reporte.paciente.id),
                reporte.imagen_conjuntiva,
            )
            exists = os.path.exists(full_path)
            print(f"   Archivo existe: {'✅ Sí' if exists else '❌ No'}")
            if not exists:
                print(f"   Buscado en: {full_path}")

                # Buscar en directorios alternativos
                alt_paths = [
                    os.path.join(
                        "static", "img", "analysis", reporte.imagen_conjuntiva
                    ),
                    os.path.join(
                        "media",
                        "analysis",
                        str(reporte.paciente.id),
                        reporte.imagen_conjuntiva,
                    ),
                ]
                for alt_path in alt_paths:
                    if os.path.exists(alt_path):
                        print(f"   ⚠️  Encontrado en: {alt_path}")

print("\n" + "=" * 80)
print("DIRECTORIOS DE ANÁLISIS EXISTENTES:")
print("=" * 80)

analysis_dir = os.path.join("static", "img", "analysis")
if os.path.exists(analysis_dir):
    subdirs = [
        d
        for d in os.listdir(analysis_dir)
        if os.path.isdir(os.path.join(analysis_dir, d))
    ]
    print(f"\nCarpetas de pacientes encontradas: {len(subdirs)}")
    for subdir in subdirs[:10]:  # Primeras 10
        path = os.path.join(analysis_dir, subdir)
        files = [f for f in os.listdir(path) if f.endswith((".jpg", ".jpeg", ".png"))]
        print(f"  - {subdir}/ ({len(files)} imágenes)")
        if files:
            print(f"    Ejemplo: {files[0]}")
else:
    print(f"\n❌ Directorio no existe: {analysis_dir}")

print("\n")
