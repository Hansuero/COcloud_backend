"""
Django settings for COcloud_backend project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-yb-8v53uclb@9b)(+x$$x3!my-_-+a%w!t2z*$x=o7_a@0wb!-"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # 'daphne',
    'channels',
    'chat',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'COcloud.apps.CocloudConfig',
    'user',
    'team',
    'message',

    'project',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "COcloud_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
ASGI_APPLICATION = 'COcloud_backend.asgi.application'
WSGI_APPLICATION = "COcloud_backend.wsgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # 连接自己的redis
            "hosts": [('82.157.165.72', 6379)],
        },
    }
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# MySQL数据库配置
mysql_ENGINE = 'django.db.backends.mysql'
mysql_NAME = 'cocloud_1'
mysql_USER = 'comusic'
mysql_PASSWORD = '2121Jizu'
mysql_HOST = '82.157.165.72'
mysql_PORT = '3306'

DATABASES = {
    'default': {
        'ENGINE': mysql_ENGINE,
        'NAME': mysql_NAME,
        'USER': mysql_USER,
        'PASSWORD': mysql_PASSWORD,
        'HOST': mysql_HOST,
        'PORT': mysql_PORT,
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# 邮件相关配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 发送邮件配置
EMAIL_HOST = 'smtp.163.com'  # 服务器名称
EMAIL_PORT = 25  # 服务端口
EMAIL_HOST_USER = 'judgement9259@163.com'  # 填写自己邮箱
EMAIL_HOST_PASSWORD = 'NNCABGNHANCKJOCK'  # 在邮箱中设置的客户端授权密码
EMAIL_FROM = 'COcloud'  # 收件人看到的发件人
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议
# EMAIL_USE_SSL = True    #是否使用SSL加密，qq企业邮箱要求使用


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
