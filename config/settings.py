from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / '.env')

# Configuração do diretório base

# Configuração do ambiente
SECRET_KEY = os.getenv('SECRET_KEY')


# Configuração do modelo de usuário personalizado
AUTH_USER_MODEL = 'configuracoes.Usuario'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'


# Configuração de modo de depuração
DEBUG = os.getenv('DEBUG')

# Configuração de hosts permitidos
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0', '*']

# Carrega hosts permitidos do .env


# Configuração de IPs internos (para uso em desenvolvimento)
INTERNAL_IPS = [
    '127.0.0.1',
]

# Configuração de aplicativos instalados
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Aplicativos locais
LOCAL_APPS = [
    'apps.configuracoes.apps.ConfiguracoesConfig',

]

# Apps de terceiros
THIRD_PARTY_APPS = [
    "debug_toolbar",

    # Adicione aqui apps de terceiros como rest_framework, etc.
]

# Configuração de aplicativos instalados
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


# Configuração de middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Configuração de URLs
ROOT_URLCONF = 'config.urls'

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.configuracoes.context_processors.empresa',
            ],
        },
    },
]
# Configuração do WSGI
WSGI_APPLICATION = 'config.wsgi.application'

BANCO_ESCOLHIDO = 1

if BANCO_ESCOLHIDO == 1:
    print('Banco de dados SQLite selecionado.')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif BANCO_ESCOLHIDO == 2:
    print('Banco de dados MySQL selecionado.')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }


# Configurações de autenticação
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

# Configurações de internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = False

# Configurações de arquivos estáticos e mídia
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Para produção (collectstatic)

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Pasta de arquivos estáticos durante desenvolvimento
]

# Configurações de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações de autenticação
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações de log

LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': BASE_DIR / 'logs' / 'django.log',
#             'when': 'midnight',
#             'interval': 1,
#             'backupCount': 30,
#             'encoding': 'utf-8',
#             'delay': True,  # <--- evita o lock inicial
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }
