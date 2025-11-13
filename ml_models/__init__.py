"""
Módulo de modelos de Machine Learning para la detección de anemia.

Este módulo contiene el modelo H5 pre-entrenado y utilidades para realizar
predicciones de anemia basadas en imágenes de la conjuntiva ocular.

Componentes:
    - model_anemia.h5: Modelo CNN entrenado (54K parámetros)
    - AnemiaDetector: Clase para cargar y usar el modelo
    
Uso básico:
    >>> from ml_models.anemia_detector import AnemiaDetector
    >>> detector = AnemiaDetector()
    >>> detector.load_model()
    >>> result = detector.predict('ruta/imagen.jpg')
    >>> print(result['diagnosis'])
"""
import os
from pathlib import Path
from django.conf import settings

# Ruta base de los modelos ML
ML_MODELS_DIR = Path(__file__).resolve().parent

# Ruta del modelo de anemia
ANEMIA_MODEL_PATH = ML_MODELS_DIR / 'model_anemia.h5'


def get_anemia_model_path():
    """
    Retorna la ruta absoluta del modelo de anemia.
    
    Returns:
        Path: Ruta al archivo model_anemia.h5
        
    Raises:
        FileNotFoundError: Si el modelo no existe
    """
    if not ANEMIA_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"El modelo de anemia no se encuentra en: {ANEMIA_MODEL_PATH}"
        )
    return ANEMIA_MODEL_PATH


def get_model_info():
    """
    Retorna información básica sobre el modelo sin cargarlo.
    
    Returns:
        dict: Información del modelo
    """
    return {
        'path': str(ANEMIA_MODEL_PATH),
        'exists': ANEMIA_MODEL_PATH.exists(),
        'size_kb': ANEMIA_MODEL_PATH.stat().st_size / 1024 if ANEMIA_MODEL_PATH.exists() else 0,
        'input_shape': '(None, 64, 64, 3)',
        'output_shape': '(None, 1)',
        'type': 'CNN - Clasificación Binaria',
        'purpose': 'Detección de anemia mediante análisis de conjuntiva ocular'
    }


# Exportar componentes principales
__all__ = [
    'ANEMIA_MODEL_PATH',
    'get_anemia_model_path',
    'get_model_info',
]
