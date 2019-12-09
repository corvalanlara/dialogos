from django.apps import AppConfig


class ActasConfig(AppConfig):
    name = 'actas'

    def ready(self):
        import actas.signals
