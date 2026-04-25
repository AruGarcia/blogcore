"""Production settings."""

from . import base


def _load_base_settings():
    return {name: getattr(base, name) for name in dir(base) if name.isupper()}


globals().update(_load_base_settings())

DEBUG = False
SECRET_KEY = base.env("SECRET_KEY")
ALLOWED_HOSTS = base.env.list("ALLOWED_HOSTS")

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
