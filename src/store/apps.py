from django.apps import AppConfig
from django.db.models.signals import post_save

from store.signals import customer_rating_post_save


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        post_save.connect(customer_rating_post_save, sender='store.CustomerRating')
