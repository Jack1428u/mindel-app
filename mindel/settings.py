import dj_database_url
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-dev')

# DEBUG debe ser False en Render.
# Se asume que en Render tienes la variable de entorno RENDER=true
DEBUG = 'RENDER' not in os.environ

# === 1. CORRECCIÓN CRÍTICA: ALLOWED_HOSTS ===
# Si estamos en Render, obtenemos el host automáticamente.
if not DEBUG:
    ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
else:
    ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceros necesarias
    'storages', # Para S3
    # Tus apps
    'courses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise debe ir justo después de SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # NOTA: Se eliminó CorsMiddleware porque no usas React externo.
]

ROOT_URLCONF = 'mindel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Asegúrate de tener tu carpeta templates aquí si la usas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mindel.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'es-pe' # Puedes poner 'es-pe' o 'es-es'
TIME_ZONE = 'America/Lima' # Ajustado a tu región
USE_I18N = True
USE_TZ = True


# === ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES DEL SISTEMA) ===
# Se sirven con Whitenoise desde el servidor local
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Motor de almacenamiento para Whitenoise (Compresión y caché)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# === ARCHIVOS MEDIA (SUBIDOS POR USUARIOS - PDFs, FOTOS) ===
# Se sirven con Amazon S3

# Credenciales (Desde Variables de Entorno de Render)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'mindel-app-media'
AWS_S3_REGION_NAME = 'sa-east-1'
AWS_S3_SIGNATURE_VERSION = 's3v4' # Recomendado para regiones nuevas

# Configuración S3
AWS_LOCATION = 'media' # Carpeta dentro del bucket
DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{AWS_LOCATION}/'


# Login URL
LOGIN_URL = '/signin'
LOGIN_REDIRECT_URL = 'courses' # A donde va después de loguearse
LOGOUT_REDIRECT_URL = 'home'   # A donde va después de salir


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'