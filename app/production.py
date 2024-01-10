import os

from .settings import *  # noqa
from .settings import BASE_DIR

INSTALLED_APPS += [
    "whitenoise.runserver_nostatic",
]

ALLOWED_HOSTS = (
    [
        "parking-spots.azurewebsites.net",
        "e-parking.site",
        # My local address Bra
        "91.145.153.63",
    ]
    if os.environ.get("IS_PROD")
    else []
)

CSRF_TRUSTED_ORIGINS = (
    [
        "https://parking-spots.azurewebsites.net",
        "http://e-parking.site",
        "http://91.145.153.63:3000",
    ]
    if "WEBSITE_HOSTNAME" in os.environ
    else []
)
# temporary
DEBUG = True
SECRET_KEY = os.getenv("SECRETKEY")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATIC_URL = os.environ.get("DJANGO_STATIC_URL", "/static/")
STATIC_ROOT = os.environ.get(
    "DJANGO_STATIC_ROOT", os.path.join(BASE_DIR, "staticfiles")
)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

conn_str = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]
conn_str_params = {
    pair.split("=")[0]: pair.split("=")[1] for pair in conn_str.split(" ")
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": conn_str_params["dbname"],
        "HOST": conn_str_params["host"],
        "USER": conn_str_params["user"],
        "PASSWORD": conn_str_params["password"],
    }
}
