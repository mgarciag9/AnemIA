"""
Módulo de vistas para análisis de imágenes.
"""
from .analysis_views import (
    analysis_view, 
    analyze_image, 
    get_patient_info, 
    analysis_results_view,
    save_analysis_report,
    delete_analysis_image,
    delete_analysis_report
)

__all__ = [
    'analysis_view',
    'analyze_image',
    'get_patient_info',
    'analysis_results_view',
    'save_analysis_report',
    'delete_analysis_image',
    'delete_analysis_report',
]
