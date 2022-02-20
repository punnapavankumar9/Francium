from storages.backends.azure_storage import AzureStorage

# class AzureMediaStorage(AzureStorage):
#     account_name = '<mystorageaccount>' 
#     account_key = '<mykey>'
#     azure_container = 'media'
#     expiration_secs = None

# class AzureStaticStorage(AzureStorage):
#     account_name = 'mystorageaccount'
#     account_key = '<my key>'
#     azure_container = 'static'
#     expiration_secs = None

from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    location = 'media'
    file_overwrite = False