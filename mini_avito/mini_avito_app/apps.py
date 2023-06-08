from django.apps import AppConfig


class MiniAvitoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_avito_app'

    def ready(self):
        import mini_avito_app.signals
