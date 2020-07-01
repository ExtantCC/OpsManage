#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
"""
Django settings for OpsManage project.

Generated by 'django-admin startproject' using Django 1.11.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import sys, os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType

try:
    import ConfigParser as conf
except ImportError as e:
    import configparser as conf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

config = conf.ConfigParser()
config.read(os.path.join(BASE_DIR, 'conf/opsmanage.ini'))   


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i)&2z^y%0w1o-%h3da1*$!9@5hx^dzp-_w&rx&4k6ml)l24&ev'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

REDSI_KWARGS_LPUSH = {"host":config.get('redis', 'host'),'port':config.get('redis', 'port'),'db':config.get('redis', 'ansible_db'),'password':config.get('redis', 'password')}
REDSI_LPUSH_POOL = None


CHANNEL_LAYERS = {
    "default": {
       "BACKEND": "channels_redis.core.RedisChannelLayer",  # use redis backend
       "CONFIG": {
            "hosts": [("redis://:" + config.get('redis', 'password') + "@"+ config.get('redis', 'host') + ":"+ config.get('redis', 'port') + "/0")]
           },
       },
}

ASGI_APPLICATION = "OpsManage.routing.application"
WSGI_APPLICATION = 'OpsManage.wsgi.application'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'mptt',
    'channels',    
    'OpsManage',
    'navbar',
    'databases',
    'asset',
    'api',
    'deploy',
    'orders',
    'wiki',
    'cicd',
    'sched',
    'django_celery_beat',
    'django_celery_results',
    'websocket',
    'apply',
    'account'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),             
}

MEDIA_ROOT = os.path.join(BASE_DIR,'upload/')

WORKSPACES = config.get('deploy', 'path')

ROOT_URLCONF = 'OpsManage.urls'

AUTH_USER_MODEL = 'account.User'

AUTHENTICATION_BACKENDS = (
    'apps.account.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



if config.get('db', 'engine') == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config.get('db', 'database'),
            'USER': config.get('db', 'user'),
            'PASSWORD': config.get('db', 'password'),
            'HOST': config.get('db', 'host'),
            'PORT': config.getint('db', 'port'),
#             'CONN_MAX_AGE': 3600, #value which is less than wait_timeout in MySQL config (my.cnf).
        }
    }
elif config.get('db', 'engine') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': config.get('db', 'database'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

INCEPTION_CONFIG = {}
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False



STATIC_URL = '/static/'
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, "static"), 
] 


if config.get('ldap', 'enable') == 'true':
    ldap_filter = config.get('ldap', 'filter')
    if ldap_filter == "OpenLDAP":
        ldap_filter = '(cn=%(user)s)' 
    else:
        ldap_filter = '(sAMAccountName=%(user)s)'  
          
    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )
    
    AUTH_LDAP_SERVER_URI = "ldap://{server}:{port}".format(server=config.get('ldap', 'server'),port=config.get('ldap', 'port')) #配置ldap的服务地址
    AUTH_LDAP_BIND_DN =  "{bind_dn}".format(bind_dn=config.get('ldap', 'bind_dn'))  #"cn=root,dc=opsmanage,dc=com"
    AUTH_LDAP_BIND_PASSWORD = "{password}".format(password=config.get('ldap', 'bind_password'))
    AUTH_LDAP_USER_SEARCH = LDAPSearch("{search_dn}".format(search_dn=config.get('ldap', 'search_dn')), ldap.SCOPE_SUBTREE, ldap_filter)
    AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr='cn')
    AUTH_LDAP_USER_ATTR_MAP = {  
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail"
    } 
    AUTH_LDAP_ALWAYS_UPDATE_USER = True
    


if config.get('inception', 'enable') == 'true':
    INCEPTION_CONFIG = {
                 "host":config.get('inception', 'host'),
                 "port":config.get('inception', 'port'),
                 "backup_host":config.get('inception', 'backup_host'),
                 "backup_passwd":config.get('inception', 'backup_passwd'),
                 "backup_user":config.get('inception', 'backup_user'),
                 "backup_port":config.get('inception', 'backup_port')
                 }
    
        

