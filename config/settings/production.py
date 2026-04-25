"""Production settings."""

from . import base


def _load_base_settings():
    return {name: getattr(base, name) for name in dir(base) if name.isupper()}


globals().update(_load_base_settings())

DEBUG = False
SECRET_KEY = base.env("SECRET_KEY")
ALLOWED_HOSTS = base.env.list("ALLOWED_HOSTS")

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
