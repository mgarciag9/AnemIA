"""
Gestor singleton del modelo de detección de anemia.
El modelo se carga una sola vez al iniciar Django y se reutiliza.
"""

from ml_models.anemia_detector import AnemiaDetector
import threading


class ModelSingleton:
    """
    Singleton para mantener una única instancia del detector de anemia cargado en memoria.
    """

    _instance = None
    _lock = threading.Lock()
    _detector = None
    _loading = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def get_detector(self):
        """
        Retorna el detector de anemia, cargándolo si es necesario.
        Thread-safe.

        Returns:
            AnemiaDetector: Instancia del detector con el modelo cargado
        """
        if self._detector is None:
            with self._lock:
                if self._detector is None and not self._loading:
                    self._loading = True
                    try:
                        print("🔄 Cargando modelo de anemia por primera vez...")
                        self._detector = AnemiaDetector()
                        self._detector.load_model()
                        print("✅ Modelo de anemia cargado y listo para usar")
                    except Exception as e:
                        print(f"❌ Error al cargar el modelo: {e}")
                        self._loading = False
                        raise
                    finally:
                        self._loading = False

        return self._detector

    def is_loaded(self):
        """
        Verifica si el modelo ya está cargado.

        Returns:
            bool: True si el modelo está cargado
        """
        return self._detector is not None

    def reload_model(self):
        """
        Recarga el modelo desde cero.
        Útil si se actualiza el archivo del modelo.
        """
        with self._lock:
            print("🔄 Recargando modelo de anemia...")
            self._detector = None
            return self.get_detector()


# Instancia global del singleton
_model_singleton = ModelSingleton()


def get_anemia_detector():
    """
    Función helper para obtener el detector de anemia.

    Returns:
        AnemiaDetector: Detector de anemia con modelo cargado
    """
    return _model_singleton.get_detector()


def is_model_loaded():
    """
    Verifica si el modelo está cargado.

    Returns:
        bool: True si el modelo está cargado
    """
    return _model_singleton.is_loaded()


def preload_model():
    """
    Pre-carga el modelo al iniciar Django.
    Debe ser llamado en apps.py ready()
    """
    try:
        print("🚀 Iniciando pre-carga del modelo de anemia...")
        get_anemia_detector()
        print("✅ Modelo pre-cargado exitosamente")
    except Exception as e:
        print(f"⚠️  No se pudo pre-cargar el modelo: {e}")
        print("   El modelo se cargará en la primera solicitud.")
