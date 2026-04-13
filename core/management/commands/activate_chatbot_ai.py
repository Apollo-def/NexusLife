"""
Comando Django para ativar e validar o Chatbot AI após instalar dependências
Usage: python manage.py activate_chatbot_ai
"""

from django.core.management.base import BaseCommand, CommandError
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Ativa e valida o Chatbot AI (Gemini/OpenAI) após instalar dependências'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('[BOT] Ativando Chatbot AI...\n'))
        
        # Verifica Gemini
        gemini_status = self.check_gemini()
        
        # Verifica OpenAI
        openai_status = self.check_openai()
        
        # Relatório final
        self.print_report(gemini_status, openai_status)
    
    def check_gemini(self):
        """Verifica se Gemini está disponível e configurado"""
        self.stdout.write('[INFO] Verificando Google Generative AI (Gemini)...')
        
        try:
            import google.generativeai as genai
            self.stdout.write(self.style.SUCCESS('  [OK] google-generativeai instalado'))
        except ImportError:
            self.stdout.write(self.style.ERROR('  [ERRO] google-generativeai NAO instalado'))
            self.stdout.write('  Instale com: pip install google-generativeai')
            return False
        
        # Verifica API Key
        api_key = os.getenv('GEMINI_API_KEY') or getattr(settings, 'GEMINI_API_KEY', None)
        
        if not api_key:
            self.stdout.write(self.style.WARNING('  [AVISO] GEMINI_API_KEY nao configurada'))
            self.stdout.write('  Configure no arquivo .env: GEMINI_API_KEY=sua-chave-aqui')
            return False
        
        if api_key.startswith('AIzaSy'):
            self.stdout.write(self.style.SUCCESS('  [OK] GEMINI_API_KEY configurada'))
        else:
            self.stdout.write(self.style.WARNING('  [AVISO] GEMINI_API_KEY pode ser invalida'))
        
        # Testa inicialização
        try:
            from core.gemini_integration import NexusBotGemini, GEMINI_AVAILABLE
            
            if GEMINI_AVAILABLE:
                bot = NexusBotGemini()
                self.stdout.write(self.style.SUCCESS('  [OK] Gemini AI inicializado com sucesso!'))
                return True
            else:
                self.stdout.write(self.style.ERROR('  [ERRO] Gemini AI nao disponivel'))
                return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  [ERRO] Erro ao inicializar: {str(e)}'))
            return False
    
    def check_openai(self):
        """Verifica se OpenAI está disponível e configurado"""
        self.stdout.write('\n[INFO] Verificando OpenAI...')
        
        try:
            import openai
            self.stdout.write(self.style.SUCCESS('  [OK] openai instalado'))
        except ImportError:
            self.stdout.write(self.style.WARNING('  [INFO] openai NAO instalado (opcional)'))
            self.stdout.write('  Instale com: pip install openai')
            return False
        
        # Verifica API Key
        api_key = os.getenv('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)
        
        if not api_key:
            self.stdout.write(self.style.WARNING('  [AVISO] OPENAI_API_KEY nao configurada'))
            self.stdout.write('  Configure no arquivo .env: OPENAI_API_KEY=sua-chave-aqui')
            return False
        
        if api_key.startswith('sk-'):
            self.stdout.write(self.style.SUCCESS('  [OK] OPENAI_API_KEY configurada'))
        else:
            self.stdout.write(self.style.WARNING('  [AVISO] OPENAI_API_KEY pode ser invalida'))
        
        # Testa inicialização
        try:
            from core.openai_integration import NexusBotAI, OPENAI_AVAILABLE
            
            if OPENAI_AVAILABLE:
                bot = NexusBotAI()
                self.stdout.write(self.style.SUCCESS('  [OK] OpenAI inicializado com sucesso!'))
                return True
            else:
                self.stdout.write(self.style.WARNING('  [INFO] OpenAI nao disponivel'))
                return False
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  [AVISO] Erro ao inicializar: {str(e)}'))
            return False
    
    def print_report(self, gemini_status, openai_status):
        """Imprime relatório final"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('[RELATORIO] ATIVACAO DE CHATBOT AI'))
        self.stdout.write('='*60)
        
        if gemini_status or openai_status:
            self.stdout.write(self.style.SUCCESS('\n[SUCESSO] Chatbot AI ATIVADO com sucesso!\n'))
            
            if gemini_status:
                self.stdout.write('  [+] Usando: Google Generative AI (Gemini)')
            if openai_status:
                self.stdout.write('  [+] Usando: OpenAI')
            
            self.stdout.write('\n[ENDPOINTS] Disponíveis:')
            self.stdout.write('  * POST /api/chatbot/ - Enviar mensagem ao chatbot')
            self.stdout.write('  * GET /chatbot/ - Pagina do chatbot')
            
            self.stdout.write(self.style.SUCCESS('\n[PRONTO] Chatbot pronto para usar!\n'))
        else:
            self.stdout.write(self.style.WARNING('\n[AVISO] Chatbot AI nao ativado.\n'))
            self.stdout.write('Acoes recomendadas:')
            self.stdout.write('  1. Instale dependencias: pip install -r requirements.txt')
            self.stdout.write('  2. Obtenha uma API Key do Google Gemini ou OpenAI')
            self.stdout.write('  3. Configure no arquivo .env')
            self.stdout.write('  4. Execute este comando novamente: python manage.py activate_chatbot_ai')
            self.stdout.write('\n[DOCS] https://ai.google.dev/gemini-api/docs\n')
