from .base import *

INSTALLED_APPS = INSTALLED_APPS + [
    'django_browser_reload',
    'debug_toolbar',
]

MIDDLEWARE = MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django_browser_reload.middleware.BrowserReloadMiddleware',
    ]

DEBUG = True

RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False

try:
    from .local import *
except ImportError:
    pass
