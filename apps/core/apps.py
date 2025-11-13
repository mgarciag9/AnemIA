from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        """
        Se ejecuta cuando Django inicia.
        Pre-carga el modelo de ML para acelerar las primeras predicciones.
        """
        import os

        # Solo pre-cargar en el proceso principal, no en el reloader de runserver
        if (
            os.environ.get("RUN_MAIN") == "true"
            or os.environ.get("WERKZEUG_RUN_MAIN") == "true"
        ):
            try:
                from ml_models.model_loader import preload_model

                preload_model()
            except Exception as e:
                print(f"⚠️  No se pudo pre-cargar el modelo de ML: {e}")
