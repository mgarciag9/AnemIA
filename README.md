# 🩺 AnemIA Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2.7-green?logo=django&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-orange?logo=tensorflow&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS-S3-yellow?logo=amazon-aws&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql&logoColor=white)

**Sistema web médico para la detección asistida por IA de anemia mediante análisis de imágenes conjuntivales**

[Características](#-características-principales) •
[Instalación](#-instalación) •
[Configuración](#-configuración) •
[Uso](#-uso) •
[Arquitectura](#-arquitectura)

</div>

---

## 📋 Tabla de Contenidos

- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Características Principales](#-características-principales)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API y Endpoints](#-api-y-endpoints)
- [Despliegue](#-despliegue)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🎯 Acerca del Proyecto

**AnemIA Detection** es un sistema web médico diseñado para asistir en la detección temprana de anemia mediante el análisis automatizado de imágenes de la conjuntiva ocular. El sistema combina técnicas de Deep Learning con análisis médico asistido por IA generativa para proporcionar diagnósticos preliminares rápidos y precisos.

### Propósito Médico

La anemia afecta a más de 1.6 mil millones de personas en el mundo. La detección temprana es crucial para el tratamiento efectivo. Este sistema permite:

- ✅ Detección no invasiva mediante análisis visual
- ✅ Resultados preliminares en menos de 30 segundos
- ✅ Reducción de costos en screening inicial
- ✅ Acceso a diagnóstico en áreas con recursos limitados

### ⚠️ Disclaimer Médico

> **IMPORTANTE**: Este sistema proporciona diagnósticos preliminares asistidos por IA y **NO** reemplaza el criterio médico profesional. Los resultados deben ser verificados por personal médico calificado antes de tomar decisiones clínicas.

---

## ✨ Características Principales

### 🤖 Inteligencia Artificial Dual

- **TensorFlow CNN**: Modelo de red neuronal convolucional entrenado específicamente para detectar anemia

  - Precisión: ~85-90% en conjunto de validación
  - Tiempo de inferencia: <1 segundo
  - Input: Imágenes RGB 64x64 de conjuntiva ocular

- **Google Gemini AI**: Generación de diagnósticos médicos estructurados
  - Interpretación contextualizada de resultados
  - Recomendaciones clínicas personalizadas
  - Análisis de grado de palidez conjuntival

### 👥 Gestión de Pacientes

- CRUD completo de pacientes con información demográfica
- Historial médico de análisis por paciente
- Fotografías de perfil almacenadas en AWS S3
- IDs únicos autogenerados (Pac-XXXXX)

### 📊 Análisis de Imágenes

- Carga y recorte interactivo de imágenes (Canvas API)
- Procesamiento automático y normalización
- Almacenamiento seguro en AWS S3
- Visualización de resultados con métricas de confianza

### 📈 Reportes Médicos

- Generación automática de reportes en PDF
- Exportación de datos históricos
- Envío de reportes por email (SMTP Gmail)
- Visualización de tendencias por paciente

### 🔐 Seguridad y Autenticación

- Sistema de autenticación basado en email
- Hashing seguro de contraseñas (PBKDF2)
- Protección CSRF en formularios
- Control de acceso basado en roles
- Sesiones seguras con Django

---

## 🛠️ Tecnologías Utilizadas

### Backend

| Tecnología     | Versión | Propósito            |
| -------------- | ------- | -------------------- |
| **Python**     | 3.13    | Lenguaje principal   |
| **Django**     | 5.2.7   | Framework web        |
| **PostgreSQL** | 16+     | Base de datos        |
| **TensorFlow** | 2.20.0  | Machine Learning     |
| **Keras**      | 3.12.0  | API ML de alto nivel |

### Cloud & Storage

| Servicio            | Uso                                          |
| ------------------- | -------------------------------------------- |
| **AWS S3**          | Almacenamiento de archivos estáticos y media |
| **Boto3**           | SDK de AWS para Python                       |
| **Django Storages** | Integración Django-S3                        |

### AI & ML

| Herramienta                 | Propósito                  |
| --------------------------- | -------------------------- |
| **Google Gemini 1.5 Flash** | Generación de diagnósticos |
| **NumPy**                   | Operaciones numéricas      |
| **Pillow**                  | Procesamiento de imágenes  |

### Otros

- **ReportLab**: Generación de PDFs
- **Python Decouple**: Gestión de variables de entorno
- **Requests**: Cliente HTTP

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### Software Requerido

- **Python 3.11+** - [Descargar](https://www.python.org/downloads/)
- **PostgreSQL 14+** - [Descargar](https://www.postgresql.org/download/)
- **pip** (gestor de paquetes Python)
- **Git** - [Descargar](https://git-scm.com/)
- **Editor de código** (VSCode, PyCharm, etc.)

### Cuentas de Servicio Necesarias

1. **Cuenta AWS** - Para almacenamiento S3

   - Acceso a IAM para crear usuarios
   - Permisos de S3

2. **Google AI Studio** - Para API de Gemini

   - Obtener API Key en [Google AI Studio](https://aistudio.google.com/)

3. **Gmail** (opcional) - Para envío de emails
   - Configurar App Password si tienes 2FA activado

### Conocimientos Recomendados

- Python básico/intermedio
- Conceptos de Django (models, views, templates)
- SQL básico
- HTML/CSS/JavaScript básico

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/anemia-detection.git
cd anemia-detection
```

### 2. Crear Entorno Virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ **Nota**: La instalación de TensorFlow (~500MB) puede tardar varios minutos.

### 4. Configurar PostgreSQL

#### Crear Base de Datos

```sql
-- Conectarse a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE anemia_project;

-- Crear usuario (opcional)
CREATE USER anemia_user WITH PASSWORD 'tu_password_seguro';

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE anemia_project TO anemia_user;

-- Salir
\q
```

### 5. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
# ========================================
# DATABASE
# ========================================
DB_ENGINE=django.db.backends.postgresql
DB_NAME=anemia_project
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# ========================================
# DJANGO
# ========================================
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ========================================
# GOOGLE GEMINI AI
# ========================================
GEMINI_API_KEY=tu_gemini_api_key_aqui
API_KEY=tu_gemini_api_key_aqui

# ========================================
# EMAIL (Gmail SMTP)
# ========================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_aqui
DEFAULT_FROM_EMAIL=noreply@anemia-detection.com

# ========================================
# AWS S3
# ========================================
USE_S3=True
AWS_ACCESS_KEY_ID=tu_access_key_id
AWS_SECRET_ACCESS_KEY=tu_secret_access_key
AWS_STORAGE_BUCKET_NAME=tu-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

#### Generar SECRET_KEY

```python
# En consola Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Configurar AWS S3

#### Crear Bucket

1. Accede a [AWS Console](https://console.aws.amazon.com/s3/)
2. Crea un nuevo bucket (ej: `anemia-detection-files`)
3. Región: `us-east-1` (o la que prefieras)
4. Desbloquear acceso público

#### Configurar CORS

Crea un archivo `cors.json`:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": ["ETag"]
  }
]
```

Aplicar CORS:

```bash
aws s3api put-bucket-cors --bucket tu-bucket-name --cors-configuration file://cors.json
```

#### Configurar Bucket Policy

Crea `bucket-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::tu-bucket-name/*"
    }
  ]
}
```

Aplicar política:

```bash
aws s3api put-bucket-policy --bucket tu-bucket-name --policy file://bucket-policy.json
```

#### Crear Usuario IAM

1. Ve a [IAM Console](https://console.aws.amazon.com/iam/)
2. Crear usuario: `anemia-s3-user`
3. Attach policy: `AmazonS3FullAccess`
4. Crear Access Keys
5. Guardar credenciales en `.env`

### 7. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 8. Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingresa:

- Email (usado como username)
- Contraseña
- Datos personales

### 9. Recopilar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

Esto subirá CSS, JS e imágenes a S3 (si `USE_S3=True`).

### 10. Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

Accede a: http://localhost:8000

---

## ⚙️ Configuración

### Configuración de Producción

Para desplegar en producción, modifica `.env`:

```env
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
SECRET_KEY=<generar-nueva-key-segura>
```

### Optimización de TensorFlow

**Problema**: TensorFlow puede tardar en cargar al iniciar.

**Solución 1 - Lazy Loading** (Recomendado para desarrollo):

```python
# apps/core/apps.py
def ready(self):
    pass  # Comentar la pre-carga
```

**Solución 2 - Pre-carga** (Recomendado para producción):

```python
# Mantener como está, la primera carga será lenta pero las siguientes rápidas
```

### Configurar Email Gmail

1. Activa verificación en 2 pasos en tu cuenta Gmail
2. Genera App Password:
   - Ve a: https://myaccount.google.com/apppasswords
   - Selecciona app: "Mail"
   - Selecciona dispositivo: "Other"
   - Copia el password generado (16 caracteres)
3. Úsalo en `EMAIL_HOST_PASSWORD` del `.env`

---

## 📖 Uso

### 1. Acceso al Sistema

#### Login

1. Ve a: http://localhost:8000/security/login/
2. Ingresa email y contraseña
3. Serás redirigido al dashboard

#### Registro

1. Ve a: http://localhost:8000/security/register/
2. Completa el formulario
3. Sube foto de perfil (opcional)
4. Inicia sesión

### 2. Gestión de Pacientes

#### Crear Paciente

1. Dashboard → "Pacientes"
2. Click en "Nuevo Paciente"
3. Completa datos:
   - DNI (único)
   - Nombre y apellido
   - Email
   - Sexo, ciudad, dirección
   - Foto de perfil (opcional)
4. Click "Guardar"

El sistema generará automáticamente un ID único (ej: `Pac-40001`).

#### Editar/Eliminar Paciente

- **Editar**: Click en ícono de lápiz
- **Eliminar**: Click en ícono de papelera (requiere confirmación)

### 3. Análisis de Imágenes

#### Realizar Análisis

1. Dashboard → "Análisis"
2. Selecciona paciente del dropdown
3. Click "Cargar Imagen"
4. Selecciona foto de conjuntiva ocular
5. **Recorta** la región de interés usando el canvas
6. Click "Analizar Imagen"
7. Espera procesamiento (~2-5 segundos)

#### Interpretación de Resultados

El sistema mostrará:

- **Predicción**: Anemia detectada / No detectada
- **Probabilidad**: 0-100% (confianza del modelo ML)
- **Nivel de Confianza**: Muy Alta, Alta, Moderada, Baja
- **Diagnóstico Gemini AI**:
  - Observaciones clínicas
  - Interpretación preliminar
  - Grado de palidez conjuntival
  - Sospecha diagnóstica
  - Recomendaciones

#### Guardar Reporte

1. En pantalla de resultados, click "Guardar Reporte"
2. Confirma fecha de análisis
3. El reporte se guarda en la base de datos
4. Accesible desde "Reportes" o perfil del paciente

### 4. Gestión de Reportes

#### Ver Reportes

- **Dashboard → Reportes**: Lista todos los reportes
- **Pacientes → [Paciente] → Ver Reportes**: Reportes de un paciente

#### Generar PDF

1. Ve a lista de reportes
2. Click en "Descargar PDF"
3. El PDF incluye:
   - Datos del paciente
   - Imagen analizada
   - Resultados ML
   - Diagnóstico completo
   - Fecha y firma digital

#### Enviar por Email

1. Ve a reporte específico
2. Click "Enviar Email"
3. Confirma destinatario
4. El reporte PDF se enviará automáticamente

### 5. Perfil de Usuario

#### Actualizar Perfil

1. Click en avatar (esquina superior derecha)
2. "Mi Perfil"
3. Edita información:
   - Nombre, apellidos
   - Foto de perfil
   - Dirección, teléfono, ciudad
4. "Guardar Cambios"

#### Cambiar Contraseña

1. Mi Perfil → "Cambiar Contraseña"
2. Ingresa:
   - Contraseña actual
   - Nueva contraseña
   - Confirmar nueva contraseña
3. "Actualizar Contraseña"

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Browser)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │   Patients   │  │   Analysis   │      │
│  │  (HTML/CSS)  │  │     (JS)     │  │   (Canvas)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   DJANGO BACKEND (5.2.7)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                     VIEWS LAYER                       │  │
│  │  • auth_views.py      • patient_views.py             │  │
│  │  • analysis_views.py  • report_views.py              │  │
│  └──────────────────────────────────────────────────────┘  │
│                             │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   BUSINESS LOGIC                      │  │
│  │  ┌────────────────┐        ┌────────────────┐        │  │
│  │  │  TensorFlow    │        │  Gemini AI     │        │  │
│  │  │  (Detection)   │───────▶│  (Diagnosis)   │        │  │
│  │  └────────────────┘        └────────────────┘        │  │
│  └──────────────────────────────────────────────────────┘  │
│                             │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    MODELS LAYER                       │  │
│  │  • CustomUser  • Paciente  • ReporteAnemia           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                    │                    │
          ┌─────────┴────────┐  ┌────────┴─────────┐
          ▼                  ▼  ▼                  ▼
┌──────────────────┐  ┌──────────────────────────────┐
│   PostgreSQL     │  │         AWS S3               │
│  ┌────────────┐  │  │  ┌────────────────────────┐ │
│  │   Users    │  │  │  │  static/               │ │
│  │  Patients  │  │  │  │  • css/  • js/        │ │
│  │  Reports   │  │  │  │  • img/  • admin/     │ │
│  └────────────┘  │  │  ├────────────────────────┤ │
│                  │  │  │  media/                │ │
│                  │  │  │  • analysis/           │ │
│                  │  │  │  • patients/           │ │
│                  │  │  │  • fotos_perfil/       │ │
└──────────────────┘  └──────────────────────────────┘
```

### Flujo de Análisis de Imagen

```
┌──────────────┐
│   Usuario    │
│ Carga Imagen │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  Canvas API (JS)     │
│  • Crop interactivo  │
│  • Convertir Base64  │
└──────┬───────────────┘
       │ POST /analysis/analyze/
       ▼
┌──────────────────────────┐
│  Django View             │
│  1. Decode Base64        │
│  2. Guardar en S3        │◄──── AWS S3
│  3. Validar imagen       │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  TensorFlow CNN          │
│  1. Preprocesar (64x64)  │
│  2. Normalizar (/255)    │
│  3. Predict              │
│  Output: Probability     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Google Gemini AI        │
│  1. Generar prompt       │
│  2. Llamar API           │
│  3. Parsear respuesta    │
│  Output: Diagnosis       │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Renderizar Resultados   │
│  • Mostrar predicción    │
│  • Mostrar diagnóstico   │
│  • Opción guardar        │
└──────────────────────────┘
       │
       ▼ (opcional)
┌──────────────────────────┐
│  Guardar en DB           │
│  • ReporteAnemia model   │
│  • Generar PDF           │
│  • Enviar email          │
└──────────────────────────┘
```

### Modelo de Datos

```sql
┌─────────────────────────────────────────────┐
│              CustomUser                      │
├─────────────────────────────────────────────┤
│ PK  id (AutoField)                          │
│ UQ  email (EmailField) ← USERNAME_FIELD     │
│     password (CharField - hashed)           │
│     first_name (CharField)                  │
│     last_name (CharField)                   │
│     profile_photo (ImageField) → S3         │
│     address, phone_number, national_id      │
│     city, gender                            │
│     is_active, is_staff, is_superuser       │
│     date_joined (DateTimeField)             │
└─────────────────────────────────────────────┘
              │
              │ 1
              │
              │ N
              ▼
┌─────────────────────────────────────────────┐
│              Paciente                        │
├─────────────────────────────────────────────┤
│ PK  id (CharField) - "Pac-XXXXX"            │
│ UQ  dni (CharField)                         │
│ UQ  correo (EmailField)                     │
│ FK  doctor_responsable → CustomUser         │
│     nombre, apellido                        │
│     sexo (M/F/O)                            │
│     ciudad, direccion                       │
│     foto_perfil (CharField) → S3            │
│     fecha_registro (DateField)              │
└─────────────────────────────────────────────┘
              │
              │ 1
              │
              │ N
              ▼
┌─────────────────────────────────────────────┐
│           ReporteAnemia                      │
├─────────────────────────────────────────────┤
│ PK  id (AutoField)                          │
│ FK  paciente → Paciente                     │
│ FK  creado_por → CustomUser                 │
│     fecha_analisis (DateField)              │
│     imagen_conjuntiva (CharField) → S3      │
│     ─────────────────────────────           │
│     tiene_anemia (BooleanField)             │
│     probabilidad (FloatField) 0-1           │
│     confianza (FloatField) 0-1              │
│     nivel_confianza (CharField)             │
│     ─────────────────────────────           │
│     observaciones_clinicas (TextField)      │
│     interpretacion_preliminar (TextField)   │
│     grado_palidez (CharField)               │
│     sospecha_diagnostica (TextField)        │
│     recomendaciones (TextField)             │
│     ─────────────────────────────           │
│     creado_en (DateTimeField)               │
└─────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
anemIA/
│
├── 📄 manage.py                    # Punto de entrada Django
├── 📄 requirements.txt             # Dependencias Python (70+ paquetes)
├── 📄 .env                         # Variables de entorno (NO subir a Git)
├── 📄 .gitignore                   # Archivos excluidos de Git
├── 📄 README.md                    # Este archivo
├── 📄 ANALISIS_COMPLETO_SISTEMA.md # Documentación técnica detallada
│
├── 📁 anemia_project/              # Configuración principal Django
│   ├── __init__.py
│   ├── settings.py                 # ⚙️ Configuración central
│   ├── urls.py                     # URLs principales
│   ├── wsgi.py                     # WSGI para producción
│   ├── asgi.py                     # ASGI para async
│   └── storage_backends.py         # Backends S3 personalizados
│
├── 📁 apps/                        # Aplicaciones Django
│   │
│   ├── 📁 core/                    # App principal (pacientes, análisis)
│   │   ├── models.py               # Modelos: Paciente, ReporteAnemia
│   │   ├── admin.py                # Configuración admin de Django
│   │   ├── apps.py                 # Configuración app (pre-carga ML)
│   │   ├── urls.py                 # URLs de core
│   │   │
│   │   ├── 📁 views/
│   │   │   ├── home/               # Dashboard
│   │   │   │   └── dashboard_views.py
│   │   │   ├── patients/           # CRUD pacientes
│   │   │   │   └── patient_views.py
│   │   │   ├── analysis/           # Análisis ML + Gemini
│   │   │   │   └── analysis_views.py
│   │   │   └── reports/            # Gestión reportes
│   │   │       └── report_views.py
│   │   │
│   │   ├── 📁 forms/
│   │   │   └── patient_forms.py    # Formularios validación
│   │   │
│   │   └── 📁 migrations/          # Migraciones de base de datos
│   │
│   └── 📁 security/                # App autenticación
│       ├── models.py               # CustomUser (basado en email)
│       ├── admin.py
│       ├── urls.py
│       │
│       ├── 📁 views/
│       │   ├── auth/               # Login, Register, Logout
│       │   │   └── auth_views.py
│       │   └── profile/            # Perfil de usuario
│       │       └── profile_views.py
│       │
│       ├── 📁 forms/
│       │   ├── auth_forms.py       # Formularios autenticación
│       │   └── profile_forms.py    # Formularios perfil
│       │
│       └── 📁 migrations/
│
├── 📁 ml_models/                   # 🤖 Sistema Machine Learning
│   ├── __init__.py
│   ├── anemia_detector.py          # Clase detector ML
│   ├── model_loader.py             # Singleton para cargar modelo
│   ├── best_model.h5               # 🎯 Modelo TensorFlow entrenado
│   └── model_anemia.h5             # Modelo alternativo
│
├── 📁 templates/                   # Templates HTML
│   ├── base.html                   # Template base con navbar/sidebar
│   │
│   ├── 📁 components/              # Componentes reutilizables
│   │   ├── navbar.html
│   │   ├── sidebar.html
│   │   ├── patient_modal.html
│   │   ├── confirm_cancel_modal.html
│   │   └── transition_modal.html
│   │
│   ├── 📁 core/
│   │   ├── dashboard.html
│   │   ├── 📁 patients/
│   │   │   └── patient_list.html
│   │   ├── 📁 analysis/
│   │   │   ├── analysis.html
│   │   │   └── analysis_results.html
│   │   └── 📁 reports/
│   │       └── report_list.html
│   │
│   └── 📁 security/
│       ├── 📁 auth/
│       │   ├── login.html
│       │   └── register.html
│       └── 📁 profile/
│           └── profile.html
│
├── 📁 static/                      # ☁️ Archivos estáticos (subidos a S3)
│   ├── 📁 css/
│   │   ├── auth.css
│   │   ├── dashboard.css
│   │   ├── patients.css
│   │   ├── analysis.css
│   │   ├── results.css
│   │   ├── modals.css
│   │   ├── typography.css
│   │   └── profile.css
│   │
│   ├── 📁 js/
│   │   ├── main.js                 # Funcionalidad global
│   │   ├── patients.js             # CRUD pacientes
│   │   ├── analysis.js             # Canvas crop, upload
│   │   ├── results.js              # Interactividad resultados
│   │   └── transition_modal.js     # Animaciones
│   │
│   └── 📁 img/                     # ⚠️ Migrar a S3 media/
│       ├── 📁 analysis/            # Imágenes de análisis
│       │   └── {paciente_id}/
│       ├── 📁 patients/            # Fotos de pacientes
│       │   └── {paciente_id}/
│       └── 📁 profile_pics/        # Fotos de perfil
│
├── 📁 staticfiles/                 # Archivos recopilados por collectstatic
│   └── (generado automáticamente)
│
└── 📁 media/                       # 📸 Archivos media (usuarios)
    ├── fotos_perfil/               # Fotos perfil usuarios
    ├── patients/                   # Fotos pacientes (futuro)
    └── analysis/                   # Imágenes análisis (futuro)
```

---

## 🔌 API y Endpoints

### Autenticación

| Método | Endpoint              | Descripción            |
| ------ | --------------------- | ---------------------- |
| `GET`  | `/security/login/`    | Formulario de login    |
| `POST` | `/security/login/`    | Procesar login         |
| `GET`  | `/security/register/` | Formulario de registro |
| `POST` | `/security/register/` | Crear usuario          |
| `POST` | `/security/logout/`   | Cerrar sesión          |

### Dashboard

| Método | Endpoint            | Descripción         |
| ------ | ------------------- | ------------------- |
| `GET`  | `/`                 | Dashboard principal |
| `GET`  | `/dashboard/stats/` | Estadísticas JSON   |

### Pacientes

| Método | Endpoint                    | Descripción       |
| ------ | --------------------------- | ----------------- |
| `GET`  | `/pacientes/`               | Listar pacientes  |
| `POST` | `/pacientes/crear/`         | Crear paciente    |
| `GET`  | `/pacientes/{id}/`          | Ver detalle       |
| `POST` | `/pacientes/{id}/editar/`   | Editar paciente   |
| `POST` | `/pacientes/{id}/eliminar/` | Eliminar paciente |

### Análisis

| Método | Endpoint                  | Descripción          |
| ------ | ------------------------- | -------------------- |
| `GET`  | `/analysis/`              | Página de análisis   |
| `POST` | `/analysis/analyze/`      | Analizar imagen (ML) |
| `GET`  | `/analysis/results/{id}/` | Ver resultados       |
| `POST` | `/analysis/save-report/`  | Guardar reporte      |

### Reportes

| Método | Endpoint                | Descripción      |
| ------ | ----------------------- | ---------------- |
| `GET`  | `/reportes/`            | Listar reportes  |
| `GET`  | `/reportes/{id}/`       | Ver reporte      |
| `GET`  | `/reportes/{id}/pdf/`   | Generar PDF      |
| `POST` | `/reportes/{id}/email/` | Enviar por email |

### Perfil

| Método | Endpoint                             | Descripción        |
| ------ | ------------------------------------ | ------------------ |
| `GET`  | `/security/profile/`                 | Ver perfil         |
| `POST` | `/security/profile/update/`          | Actualizar perfil  |
| `POST` | `/security/profile/change-password/` | Cambiar contraseña |

---

## 🚀 Despliegue

### Opción 1: AWS EC2 + RDS + S3

#### 1. Configurar EC2

```bash
# Conectar a instancia
ssh -i "tu-key.pem" ubuntu@ec2-xx-xxx-xxx-xxx.compute-1.amazonaws.com

# Instalar dependencias
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql-client

# Clonar repositorio
git clone https://github.com/tu-usuario/anemia-detection.git
cd anemia-detection

# Crear venv e instalar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 2. Configurar PostgreSQL RDS

1. Crear instancia RDS PostgreSQL
2. Configurar Security Group (puerto 5432)
3. Actualizar `.env` con endpoint RDS

```env
DB_HOST=tu-instancia.rds.amazonaws.com
DB_NAME=anemia_db
DB_USER=postgres
DB_PASSWORD=tu_password_seguro
```

#### 3. Configurar Gunicorn

```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/anemia.service
```

```ini
[Unit]
Description=AnemIA Django Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/anemia-detection
Environment="PATH=/home/ubuntu/anemia-detection/venv/bin"
ExecStart=/home/ubuntu/anemia-detection/venv/bin/gunicorn \
    --workers 3 \
    --bind 0.0.0.0:8000 \
    anemia_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar servicio
sudo systemctl start anemia
sudo systemctl enable anemia
```

#### 4. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/anemia
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        # S3 maneja los estáticos, esto es solo fallback
        alias /home/ubuntu/anemia-detection/staticfiles/;
    }
}
```

```bash
# Activar sitio
sudo ln -s /etc/nginx/sites-available/anemia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Configurar HTTPS (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

### Opción 2: Heroku

```bash
# Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Crear app
heroku create anemia-detection-app

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini

# Configurar variables
heroku config:set SECRET_KEY="tu-secret-key"
heroku config:set DEBUG=False
heroku config:set GEMINI_API_KEY="tu-api-key"
heroku config:set AWS_ACCESS_KEY_ID="tu-access-key"
# ... etc

# Deploy
git push heroku main

# Migrar DB
heroku run python manage.py migrate

# Crear superuser
heroku run python manage.py createsuperuser
```

### Opción 3: Docker

```dockerfile
# Dockerfile
FROM python:3.13-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Recopilar estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "anemia_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: "3.8"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: anemia_project
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn anemia_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

volumes:
  postgres_data:
```

```bash
# Construir y ejecutar
docker-compose up --build
```

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto:

### 1. Fork el Repositorio

```bash
git clone https://github.com/tu-usuario/anemia-detection.git
cd anemia-detection
```

### 2. Crear Rama de Feature

```bash
git checkout -b feature/nueva-funcionalidad
```

### 3. Hacer Cambios

- Escribe código limpio y documentado
- Sigue las convenciones PEP 8
- Agrega tests si es posible

### 4. Commit y Push

```bash
git add .
git commit -m "feat: Agregar nueva funcionalidad X"
git push origin feature/nueva-funcionalidad
```

### 5. Crear Pull Request

- Ve a GitHub
- Crea Pull Request desde tu rama
- Describe los cambios realizados
- Espera revisión

### Guía de Estilo

```python
# ✅ BUENO
def analyze_image(image_path: str) -> dict:
    """
    Analiza una imagen de conjuntiva para detectar anemia.

    Args:
        image_path: Ruta a la imagen a analizar

    Returns:
        Dict con resultados de la predicción
    """
    detector = get_anemia_detector()
    return detector.predict(image_path)

# ❌ MALO
def ai(i):
    d = gad()
    return d.p(i)
```

---

## 🐛 Reporte de Bugs

Si encuentras un bug:

1. Verifica que no esté ya reportado en [Issues](https://github.com/tu-usuario/anemia-detection/issues)
2. Crea un nuevo issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots (si aplica)
   - Entorno (OS, Python version, etc.)

---

## 📝 Roadmap

### v1.1 (Próximo)

- [ ] Migración completa de imágenes a S3
- [ ] Optimización de carga de TensorFlow
- [ ] Implementación de Celery para análisis async
- [ ] Dashboard con gráficos Chart.js
- [ ] Exportación de datos a Excel

### v2.0 (Futuro)

- [ ] API REST con Django REST Framework
- [ ] App móvil (React Native)
- [ ] Múltiples modelos ML seleccionables
- [ ] Sistema de permisos por roles
- [ ] Integración con sistemas hospitalarios (HL7/FHIR)
- [ ] Soporte multiidioma (i18n)

### v3.0 (Visión)

- [ ] Detección de múltiples enfermedades
- [ ] Análisis por lotes (batch processing)
- [ ] Sistema de segunda opinión médica
- [ ] Blockchain para trazabilidad de reportes
- [ ] IA explicable (XAI) con heatmaps

---

## ❓ FAQ (Preguntas Frecuentes)

### ¿El sistema puede diagnosticar anemia de forma definitiva?

**No**. El sistema proporciona un diagnóstico preliminar asistido por IA que **debe ser verificado por un médico profesional**. Es una herramienta de screening, no un reemplazo del criterio médico.

### ¿Qué precisión tiene el modelo?

El modelo CNN tiene una precisión del ~85-90% en el conjunto de validación. Sin embargo, la precisión puede variar según la calidad de la imagen y las condiciones de captura.

### ¿Por qué tarda tanto en cargar TensorFlow?

TensorFlow 2.20.0 es un framework pesado (~500MB). La primera carga puede tardar 15-30 segundos. Para desarrollo, puedes usar lazy loading. En producción, se pre-carga una sola vez.

### ¿Puedo usar el sistema sin AWS S3?

Sí. Configura `USE_S3=False` en `.env`. Los archivos se guardarán localmente en `/static/` y `/media/`. No recomendado para producción.

### ¿Es gratuito?

El software es de código abierto. Sin embargo:

- **AWS S3**: Free Tier (12 meses), luego ~$0.01-0.02/mes
- **Google Gemini**: Free Tier generoso, luego pago por token
- **Hosting**: Depende del proveedor

### ¿Cómo actualizo el modelo ML?

1. Entrena un nuevo modelo y guárdalo como `.h5`
2. Reemplaza `ml_models/best_model.h5`
3. Reinicia el servidor Django
4. El nuevo modelo se cargará automáticamente

### ¿Puedo personalizar el diagnóstico de Gemini?

Sí. Edita el prompt en `apps/core/views/analysis/analysis_views.py`:

```python
prompt = f"""
Tu prompt personalizado aquí...
"""
```

### ¿Cómo hago backup de la base de datos?

```bash
# PostgreSQL
pg_dump -U postgres anemia_project > backup_$(date +%Y%m%d).sql

# Restaurar
psql -U postgres anemia_project < backup_20251112.sql
```

---

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License**.

```
MIT License

Copyright (c) 2025 AnemIA Detection Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👥 Autores

- **Miguel García** - _Desarrollo inicial_ - [mgarciag9@unemi.edu.ec](mailto:mgarciag9@unemi.edu.ec)

---

## 🙏 Agradecimientos

- **TensorFlow Team** - Framework de Machine Learning
- **Google AI** - Gemini API para diagnósticos
- **Django Software Foundation** - Framework web robusto
- **AWS** - Infraestructura en la nube
- **Comunidad Open Source** - Librerías y herramientas

---

## 📞 Soporte y Contacto

- **Email**: mgarciag9@unemi.edu.ec
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/anemia-detection/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/anemia-detection/wiki)

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

[⬆ Volver arriba](#-anemia-detection-system)

---

Hecho con ❤️ por el equipo de AnemIA Detection

</div>
