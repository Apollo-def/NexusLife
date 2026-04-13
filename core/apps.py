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
        
        # Inicializa o Chatbot AI (Gemini) quando o app Django estiver pronto.
        self.initialize_chatbot_ai()
        
        # Registra signals para notificações e emails automáticos
        from . import signals
    
    def initialize_chatbot_ai(self):
        """Inicializa o Chatbot AI com Gemini ou OpenAI"""
        try:
            from .gemini_integration import GEMINI_AVAILABLE, NexusBotGemini
            from .openai_integration import OPENAI_AVAILABLE, NexusBotAI
            import logging
            
            logger = logging.getLogger(__name__)
            
            if GEMINI_AVAILABLE:
                try:
                    gemini_bot = NexusBotGemini()
                    logger.info("[OK] Chatbot AI ativado: Gemini AI inicializado com sucesso!")
                except Exception as e:
                    logger.warning(f"[AVISO] Erro ao inicializar Gemini AI: {str(e)}")
            elif OPENAI_AVAILABLE:
                try:
                    openai_bot = NexusBotAI()
                    logger.info("[OK] Chatbot AI ativado: OpenAI inicializado com sucesso!")
                except Exception as e:
                    logger.warning(f"[AVISO] Erro ao inicializar OpenAI: {str(e)}")
            else:
                logger.info("[INFO] Chatbot AI nao disponível. Usando respostas do dicionário.")
                logger.info("[INFO] Para ativar IA: instale google-generativeai ou openai")
                logger.info("[INFO] Defina GEMINI_API_KEY ou OPENAI_API_KEY no arquivo .env")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Erro ao inicializar Chatbot AI: {str(e)}")
