from django.apps import AppConfig


class EventhubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventHub'

    def ready(self):
        import eventHub.signals
