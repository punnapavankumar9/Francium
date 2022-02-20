import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ["DJANGO_PROJECT_FRANCIUM_SECRET_KEY"]

DEBUG = True

ALLOWED_HOSTS = ['francium.azurewebsites.net', '127.0.0.1']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "francium",
        "USER": "punnapavankumar9@francium-db",
        "PASSWORD": os.getenv("AZURE_FRANCIUM_DB_PASSWORD"),
        "HOST":"francium-db.postgres.database.azure.com",
        "PORT": "5432",
        "OPTIONS":{"sslmode":"require"}
    }
}

STATICFILES_DIRS = [
    BASE_DIR / 'static/'
]

AZURE_ACCOUNT_NAME = 'franciumstorage'
AZURE_ACCOUNT_KEY = os.getenv("AZURE_FRANCIUM_STORAGE_ACCOUNT_KEY")

AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
AZURE_LOCATION = ''
AZURE_CONTAINER = 'media'
AZURE_SSL = True
AZURE_URL_EXPIRATION_SECS = 600
DEFAULT_FILE_STORAGE = 'francium.custom_azure.AzureMediaStorage'


STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
