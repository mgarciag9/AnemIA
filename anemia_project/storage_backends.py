"""
Custom storage backends para AWS S3
Separa archivos estáticos de archivos media (uploads de usuarios)
"""

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Storage para archivos estáticos (CSS, JS, etc.)"""

    location = "static"
    file_overwrite = True


class PublicMediaStorage(S3Boto3Storage):
    """Storage para archivos media (imágenes de pacientes, etc.)"""

    location = "media"
    file_overwrite = False
