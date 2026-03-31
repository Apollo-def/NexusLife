from django.apps import AppConfig

# Esta classe de configuração permite ao Django saber sobre o aplicativo 'core' e suas configurações.
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Correção de bug conhecido no Django 4.2.29 + Python 3.14:
        # BaseContext.__copy__ falha ao usar copy(super()) e causa erro em admin change_form.
        try:
            from django.template import context as template_context

            def _fixed_basecontext_copy(self):
                duplicate = object.__new__(self.__class__)
                # copia os atributos existentes para preservar comportamento de subclasses
                duplicate.__dict__.update(getattr(self, '__dict__', {}))
                duplicate.dicts = self.dicts[:]
                return duplicate

            template_context.BaseContext.__copy__ = _fixed_basecontext_copy
        except Exception:
            pass

        # Inicializa o Firebase Admin SDK quando o app Django estiver pronto.
        from . import firebase_config
        firebase_config.initialize_firebase_admin()
