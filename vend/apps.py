from django.apps import AppConfig

class VendConfig(AppConfig):
    name = 'vend'

    def ready(self):
        from .signals import handlers