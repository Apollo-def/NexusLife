from django.apps import AppConfig

# Esta classe de configuração permite ao Django saber sobre o aplicativo 'core' e suas configurações.
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Inicializa o Firebase Admin SDK quando o app Django estiver pronto.
        from . import firebase_config
        firebase_config.initialize_firebase_admin()
