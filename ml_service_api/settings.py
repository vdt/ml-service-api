"""
Local settings file
"""
import sys
import os
from path import path

#Initialize celery
import djcelery
djcelery.setup_loader()

# Django settings for ml_service_api project.
ROOT_PATH = path(__file__).dirname()
REPO_PATH = ROOT_PATH.dirname()
ENV_ROOT = REPO_PATH.dirname()

#ML Specific settings
ML_PATH = os.path.join(ENV_ROOT, "machine-learning/") #Path to ML repo containing grade.py and create.py
ML_MODEL_PATH=os.path.join(ENV_ROOT,"ml_models_api/") #Path to save and retrieve ML models from
TIME_BETWEEN_ML_CREATOR_CHECKS= 1 * 60 # seconds.  Time between ML creator checking to see if models need to be made.
TIME_BETWEEN_ML_GRADER_CHECKS= 10 # seconds.  Time between ML grader checking to see if models need to be made.
USE_S3_TO_STORE_MODELS= False #Determines whether or not models are placed in Amazon S3
S3_BUCKETNAME="OpenEnded"
TIME_BEFORE_REMOVING_STARTED_MODEL = 10 * 60 * 60 # in seconds, time before removing an ml model that was started (assume it wont finish)

LOGIN_REDIRECT_URL = "/frontend/"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '../db/service-api-db.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(REPO_PATH / "staticfiles")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(REPO_PATH / 'css_js_src/'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_JS = {
    'util' : {
        'source_filenames': [
            'js/jquery-1.9.1.js',
            'js/json2.js',
            'js/underscore.js',
            'js/backbone.js',
            'js/backbone.validations.js',
            'js/backbone-tastypie.js',
            'js/backbone-schema.js',
            'js/setup-env.js',
            'js/api-views.js',
            'js/jquery.cookie.js',
            ],
        'output_filename': 'js/util.js',
    }
}

API_MODELS = ["userprofile", "user", "membership", "course", "organization", "problem", "essay", "essaygrade"]

for model in API_MODELS:
    PIPELINE_JS[model] = {
        'source_filenames': [
            'js/views/{0}.js'.format(model)
        ],
        'output_filename': 'js/{0}.js'.format(model),
    }

PIPELINE_CSS = {
    'skeleton': {
        'source_filenames': [
            'css/skeleton.css',
            'css/base.css',
            'css/layout.css',
            ],
        'output_filename': 'css/skeleton.css',
        },
}


PIPELINE_DISABLE_WRAPPER = True
PIPELINE_YUI_BINARY = "yui-compressor"

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

PIPELINE_COMPILE_INPLACE = True
PIPELINE = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u)4v9b&amp;9jhsg-&amp;&amp;^*!jff&amp;t1e7$em0uh8^i^w!ojjvr&amp;8$ok6-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'request_provider.middleware.RequestProvider',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'ml_service_api.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ml_service_api.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(REPO_PATH / "templates"),
    os.path.abspath(REPO_PATH / "freeform_data")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'tastypie',
    'freeform_data',
    'south',
    'ml_grading',
    'djcelery',
    'pipeline',
    'guardian',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

syslog_format = ("[%(name)s][env:{logging_env}] %(levelname)s "
                 "[{hostname}  %(process)d] [%(filename)s:%(lineno)d] "
                 "- %(message)s").format(
    logging_env="", hostname="")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(process)d '
                      '[%(name)s] %(filename)s:%(lineno)d - %(message)s',
            },
        'syslog_format': {'format': syslog_format},
        'raw': {'format': '%(message)s'},
        },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout,
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
            },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        }
}

AUTH_PROFILE_MODULE = 'freeform_data.UserProfile'

BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
