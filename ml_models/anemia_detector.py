"""
Utilidad para cargar y utilizar el modelo de detección de anemia.
"""
import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path


class AnemiaDetector:
    """
    Clase para la detección de anemia mediante análisis de imágenes de conjuntiva.
    """
    
    def __init__(self, model_path='ml_models/best_model.h5'):
        """
        Inicializa el detector de anemia.
        
        Args:
            model_path (str): Ruta al archivo del modelo H5
        """
        self.model_path = Path(model_path)
        self.model = None
        self.input_size = (64, 64)
        self.threshold = 0.5  # Umbral de decisión por defecto
        
    def load_model(self):
        """Carga el modelo de TensorFlow."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado en: {self.model_path}")
        
        self.model = tf.keras.models.load_model(str(self.model_path))
        print(f"Modelo cargado exitosamente desde {self.model_path}")
        print(f"   Input shape: {self.model.input_shape}")
        print(f"   Output shape: {self.model.output_shape}")
        
    def preprocess_image(self, image_path_or_array):
        """
        Preprocesa una imagen para el modelo.
        
        Args:
            image_path_or_array: Ruta a la imagen o array numpy
            
        Returns:
            np.ndarray: Imagen preprocesada lista para predicción
        """
        # Cargar imagen si es una ruta
        if isinstance(image_path_or_array, (str, Path)):
            img = Image.open(image_path_or_array)
        elif isinstance(image_path_or_array, Image.Image):
            img = image_path_or_array
        else:
            # Asumir que es un array numpy
            img = Image.fromarray(image_path_or_array)
        
        # Convertir a RGB si es necesario
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar a 64x64
        img = img.resize(self.input_size)
        
        # Convertir a array y normalizar
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Añadir dimensión de batch
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image_path_or_array, return_probability=False):
        """
        Realiza una predicción sobre una imagen.
        
        Args:
            image_path_or_array: Ruta a la imagen o array numpy
            return_probability (bool): Si True, retorna la probabilidad cruda
            
        Returns:
            dict: Resultado de la predicción con información detallada
        """
        if self.model is None:
            self.load_model()
        
        # Preprocesar imagen
        img_array = self.preprocess_image(image_path_or_array)
        
        # Realizar predicción
        prediction = self.model.predict(img_array, verbose=0)
        probability = float(prediction[0][0])
        
        # Clasificar según umbral
        has_anemia = probability >= self.threshold
        
        # Calcular nivel de confianza
        confidence = probability if has_anemia else (1 - probability)
        
        result = {
            'has_anemia': has_anemia,
            'probability': probability,
            'confidence': confidence,
            'diagnosis': 'Anemia detectada' if has_anemia else 'No se detectó anemia',
            'confidence_level': self._get_confidence_level(confidence)
        }
        
        return result
    
    def predict_batch(self, image_paths):
        """
        Realiza predicciones sobre múltiples imágenes.
        
        Args:
            image_paths (list): Lista de rutas de imágenes
            
        Returns:
            list: Lista de resultados de predicciones
        """
        results = []
        for img_path in image_paths:
            result = self.predict(img_path)
            result['image_path'] = str(img_path)
            results.append(result)
        return results
    
    def _get_confidence_level(self, confidence):
        """
        Determina el nivel de confianza en palabras.
        
        Args:
            confidence (float): Valor de confianza (0-1)
            
        Returns:
            str: Nivel de confianza en palabras
        """
        if confidence >= 0.9:
            return 'Muy alta'
        elif confidence >= 0.75:
            return 'Alta'
        elif confidence >= 0.6:
            return 'Moderada'
        else:
            return 'Baja'
    
    def set_threshold(self, threshold):
        """
        Ajusta el umbral de decisión.
        
        Args:
            threshold (float): Nuevo umbral (0-1)
        """
        if not 0 <= threshold <= 1:
            raise ValueError("El umbral debe estar entre 0 y 1")
        self.threshold = threshold
        print(f"✅ Umbral de decisión ajustado a: {threshold}")
    
    def get_model_info(self):
        """
        Retorna información sobre el modelo.
        
        Returns:
            dict: Información del modelo
        """
        if self.model is None:
            self.load_model()
        
        return {
            'model_name': self.model.name,
            'input_shape': self.model.input_shape,
            'output_shape': self.model.output_shape,
            'total_params': self.model.count_params(),
            'num_layers': len(self.model.layers),
            'threshold': self.threshold
        }


# Ejemplo de uso
if __name__ == '__main__':
    # Crear detector
    detector = AnemiaDetector()
    
    # Cargar modelo
    detector.load_model()
    
    # Mostrar información del modelo
    info = detector.get_model_info()
    print("\n📊 Información del Modelo:")
    for key, value in info.items():
        print(f"   {key}: {value}")
    