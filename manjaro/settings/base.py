import os, time
from django.core.management.utils import get_random_secret_key
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class StaticFilesOverride(ManifestStaticFilesStorage):
    manifest_strict = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

if "DEBUG" in os.environ:
    DEBUG = os.environ.get("DEBUG")
else:
    DEBUG = True

HARDWARE_NOISE = os.urandom(10)
SECRET_KEY = get_random_secret_key() + HARDWARE_NOISE.hex() + str(time.time()) + get_random_secret_key()

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

INSTALLED_APPS = [
    'home',
    'search',
    'customblocks', 
    'wagtailyoast',
    'menus',
    'dashboard',
    'contact',
    'captcha',
    'wagtailcaptcha',
    'users',
    'django.contrib.auth',
    'wagtail.contrib.sitemaps',
    'wagtail.contrib.routable_page',
    'django_social_share',
    'puput',
    'colorful',
    'tailwind',
    'theme',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wagtail.contrib.modeladmin',
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'manjaro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'manjaro.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

LANGUAGE_CODE = 'en-us'

WY_LOCALE = LANGUAGE_CODE

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

WHITENOISE_MANIFEST_STRICT = False

STATICFILES_STORAGE = 'manjaro.settings.base.StaticFilesOverride'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

WAGTAIL_SITE_NAME = "manjaro"

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

BASE_URL = 'manjaro.org'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

NOCAPTCHA = True

PUPUT_AS_PLUGIN = True

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]

AUTH_USER_MODEL = 'users.User'
WAGTAIL_USER_EDIT_FORM = 'users.admin.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'users.admin.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['position', 'description', 'title', "avatar", "tweeter", "github", "bio"]