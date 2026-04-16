import sys
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

        # Inicializa o Chatbot AI apenas em tempo de execução do servidor, não durante migrate/test/shell.
        if len(sys.argv) > 1 and sys.argv[1] in ('runserver', 'runserver_plus', 'uwsgi', 'gunicorn', 'daphne'):
            self.initialize_chatbot_ai()

        # Registra signals para notificações e emails automáticos
        from . import signals
    
    def initialize_chatbot_ai(self):
        """Inicializa o Chatbot AI com Gemini ou OpenAI"""
        try:
            from .gemini_integration import GEMINI_AVAILABLE, NexusBotGemini
            # Removed unused OpenAI import
            import logging
            
            logger = logging.getLogger(__name__)
            
            if GEMINI_AVAILABLE:
                try:
                    gemini_bot = NexusBotGemini()
                    logger.info("[OK] Chatbot AI ativado: Gemini AI inicializado com sucesso!")
                except Exception as e:
                    logger.warning(f"[AVISO] Erro ao inicializar Gemini AI: {str(e)}")
            else:
                    logger.info("[INFO] Gemini não disponível. Usando respostas básicas do chatbot.")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Erro ao inicializar Chatbot AI: {str(e)}")
