from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]  # later add domain Render

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_DB_PORT"),
        'OPTIONS': {
            "sslmode": "require"
        }
    }
}