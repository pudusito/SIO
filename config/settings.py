from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# cargamos como variables de entorno (S.O) todas las del archivo .env
load_dotenv(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', '').split(',')]


# Application definition
INSTALLED_APPS = [
    # Apps por defecto
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps del proyecto
    'apps.pacientes',
    'apps.partos',
    'apps.perfiles',
    'apps.recien_nacidos',
    'apps.reportes',
    'apps.auditoria',
    'theme',
    'apps.dashboard',
    # Apps de terceros,
    'dal',
    'dal_select2',
    'simple_history',
    'formtools',

]

TAILWIND_APP_NAME = 'theme'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middlewares Propios
    'apps.perfiles.middlewares.FirstLoginMiddleware',
    'apps.perfiles.middlewares.VerificacionEmailMiddleware',
    # Middlewares de Terceros
    'simple_history.middleware.HistoryRequestMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "templates", BASE_DIR / "errors"],
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

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTENTICACION
AUTH_USER_MODEL = 'perfiles.Usuario'

LOGIN_REDIRECT_URL = 'pantalla_principal'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Urls que puede acceder cualquier usuario, a traves de los middlewares
PUBLIC_URLS = [
    '/admin',
    '/login', 
    '/perfiles/modificar-password', 
    '/perfiles/verificacion-email',] 


if not DEBUG:
    # Si no estamos en desarrollo usamos el servidor de correos para autenticarnos
    # y mandar correos a cuentas reales
    EMAIL_HOST=os.environ.get("EMAIL_HOST")
    EMAIL_PORT=int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_USE_TLS=os.environ.get("EMAIL_USE_TLS") == "True"
    EMAIL_HOST_USER=os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD=os.environ.get("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL=EMAIL_HOST_USER
    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
    # Base de datos para producción 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'PASSWORD': os.getenv('DB_PASSWORD')
        }
    }


# Configuraciones de desarrollo
else:
    INSTALLED_APPS.extend(['django_extensions', 'tailwind'])
    # Ruta NPM para compilar el archivo o generar el archivo css con las clases que use de tailwind
    NPM_BIN_PATH= os.environ.get('NPM_BIN_PATH', '')
    EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
    # Base de datos para desarrollo (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    