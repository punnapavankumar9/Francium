import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ["DJANGO_PROJECT_FRANCIUM_SECRET_KEY"]

DEBUG = False

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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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

# STATIC_LOCATION = 'static'
# STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
DEFAULT_FILE_STORAGE = 'francium.custom_azure.AzureMediaStorage'


STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# DEFAULT_FILE_STORAGE = 'backend.custom_azure.AzureMediaStorage'
# STATICFILES_STORAGE = 'backend.custom_azure.AzureStaticStorage'

# STATIC_LOCATION = "static"
# AZURE_ACCOUNT_NAME = 'franciumstorage'
# MEDIA_LOCATION = f"http://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/media"
# MEDIA_ROOT='http://{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

# AZURE_ACCOUNT_KEY = os.getenv("AZURE_FRANCIUM_STORAGE_ACCOUNT_KEY")
# AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
# AZURE_LOCATION=f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

# STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
# MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
