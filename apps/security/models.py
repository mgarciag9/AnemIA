from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,  # <-- Importar Group
    Permission,  # <-- Importar Permission
)
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email debe ser proporcionado")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Correo electrónico", unique=True, max_length=255
    )
    first_name = models.CharField(
        verbose_name="Nombre(s)", max_length=150
    )
    last_name = models.CharField(
        verbose_name="Apellido(s)", max_length=150
    )
    profile_photo = models.ImageField(
        verbose_name="Foto de perfil",
        upload_to="fotos_perfil/",
        null=True,
        blank=True,
        db_column="foto_perfil",
    )
    address = models.CharField(
        verbose_name="Dirección", max_length=255, blank=True, db_column="direccion"
    )
    phone_number = models.CharField(
        verbose_name="Número de teléfono", max_length=20, blank=True, db_column="telefono"
    )
    national_id = models.CharField(
        verbose_name="DNI", max_length=20, blank=True, db_column="dni"
    )
    city = models.CharField(
        verbose_name="Ciudad", max_length=100, blank=True, db_column="ciudad"
    )
    gender = models.CharField(
        verbose_name="Sexo", max_length=10, blank=True, db_column="sexo"
    )
    
    is_active = models.BooleanField(verbose_name="Activo", default=True)
    is_staff = models.BooleanField(verbose_name="Staff", default=False)
    is_superuser = models.BooleanField(verbose_name="Superusuario", default=False)
    
    date_joined = models.DateTimeField(
        verbose_name="Fecha de Registro", default=timezone.now
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name="Grupos",
        blank=True,
        help_text=(
            "Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos "
            "otorgados a cada uno de sus grupos."
        ),
        related_name="custom_user_set"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="Permisos de usuario",
        blank=True,
        help_text="Permisos específicos para este usuario.",
        related_name="custom_user_permissions_set"
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def get_short_name(self):
        return self.first_name or self.email
    
    def get_display_name(self):
        """Retorna el primer nombre y los apellidos completos"""
        if self.first_name and self.last_name:
            # Obtener solo el primer nombre
            primer_nombre = self.first_name.split()[0] if self.first_name else ""
            return f"{primer_nombre} {self.last_name}".strip()
        return self.email