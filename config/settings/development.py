"""Development settings."""

from . import base


def _load_base_settings():
    return {name: getattr(base, name) for name in dir(base) if name.isupper()}


globals().update(_load_base_settings())

DEBUG = base.env("DEBUG", default=True)
SECRET_KEY = base.env(
    "SECRET_KEY",
    default="django-insecure-dev-only-key-change-me",
)
ALLOWED_HOSTS = base.env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])
