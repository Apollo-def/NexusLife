"""
Integração com Google Gemini AI para o Chatbot NexusLife
Provides advanced AI responses with conversation memory
"""

import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Generative AI não instalado. Instale com: pip install google-generativeai")


class NexusBotGemini:
    """Gerenciador de IA Gemini para o NexusBot"""
    
    def __init__(self):
        """Inicializa o cliente Gemini"""
        self.api_key = os.getenv('GEMINI_API_KEY') or getattr(settings, 'GEMINI_API_KEY', None)
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY não configurada")
            self.api_key = None
        else:
            genai.configure(api_key=self.api_key)
        
        # Usar o modelo mais recente e estável do Gemini
        self.model_name = "gemini-2.5-flash"
        self.temperature = 0.7
        self.max_tokens = 500
        
    def get_system_prompt(self, user_profile=None):
        """Cria o prompt do sistema com contexto do usuário"""
        
        base_prompt = """Você é o NexusBot, um assistente inteligente da plataforma NexusLife.
        
A NexusLife é uma plataforma de marketplace de serviços freelancer que conecta:
- Pessoa Física (PF): Freelancers que oferecem serviços digitais (designers, programadores, redatores, etc)
- Pessoa Jurídica (PJ): Empresas que contratam freelancers para projetos

IMPORTANTES - Sempre siga estas diretrizes:
1. Responda sempre em português brasileiro
2. Seja amigável, profissional e prestativo
3. Respostas devem ser concisas (máximo 300 palavras)
4. Mencione recursos específicos: /profile/, /marketplace/, /dashboard/
5. Para PF: fale sobre como criar serviços, receber pedidos, avaliações
6. Para PJ: fale sobre contratar freelancers, gerenciar projetos
7. Mantenha o contexto das conversas anteriores
8. Se não souber algo específico da plataforma, diga que pode ajudar com informações gerais

TÓPICOS QUE VOCÊ PODE AJUDAR:
- Cadastro e registro (PF/PJ)
- Como usar o marketplace
- Criação e gerenciamento de serviços
- Contratação de freelancers
- Dashboards (PF em /marketplace/dashboard/pf/, PJ em /marketplace/dashboard/pj/)
- Sistema de avaliações (reviews 1-5 estrelas)
- Favoritos e salvos
- Pedidos e projetos
- Segurança e confiança na plataforma
        """
        
        # Adiciona contexto do usuário se disponível
        if user_profile:
            user_context = f"""
CONTEXTO DO USUÁRIO ATUAL:
- Tipo de conta: {user_profile.get('person_type', 'Não definido')}
- Avaliação: {user_profile.get('average_rating', 0)}/5.0 ⭐
- Taxa de conclusão: {user_profile.get('completion_rate', 0)}%
- Ganhos: R$ {user_profile.get('total_earnings', 0):.2f}

Personalize suas respostas baseado no tipo de conta do usuário (PF = freelancer, PJ = contratante).
            """
            base_prompt += user_context
        
        return base_prompt
    
    def process_message(self, message, conversation_history=None, user_profile=None):
        """
        Processa uma mensagem e retorna a resposta do Gemini
        
        Args:
            message: Mensagem do usuário
            conversation_history: Lista de mensagens anteriores [{role, content}, ...]
            user_profile: Perfil do usuário para contexto
            
        Returns:
            dict: {
                'response': str (resposta do bot),
                'error': str (erro se houver)
            }
        """
        
        if not GEMINI_AVAILABLE or not self.api_key:
            return {
                'response': None,
                'error': 'Gemini AI não está disponível. Configure GEMINI_API_KEY nas variáveis de ambiente.'
            }
        
        try:
            # Inicializar o modelo
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self.get_system_prompt(user_profile),
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                ),
            )
            
            # Construir histórico de conversas para o Gemini
            chat_history = []
            
            if conversation_history:
                for msg in conversation_history:
                    role = "user" if msg.get('role') == 'user' else 'model'
                    chat_history.append({
                        'role': role,
                        'parts': [msg.get('content', '')]
                    })
            
            # Iniciar sessão de chat
            chat = model.start_chat(history=chat_history)
            
            # Enviar mensagem
            response = chat.send_message(message)
            
            # Extrair texto da resposta
            bot_response = response.text if response.text else "Desculpe, não consegui gerar uma resposta."
            
            return {
                'response': bot_response,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar com Gemini: {str(e)}")
            return {
                'response': None,
                'error': f'Erro ao processar sua mensagem: {str(e)}'
            }


# Instância global
try:
    gemini_bot_ai = NexusBotGemini()
except Exception as e:
    logger.error(f"Erro ao inicializar Gemini: {e}")
    gemini_bot_ai = None
