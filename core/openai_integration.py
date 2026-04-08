"""
Integração com OpenAI para o Chatbot NexusLife
Provides advanced AI responses with conversation memory
"""

import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI não instalado. Instale com: pip install openai")


class NexusBotAI:
    """Gerenciador de IA para o NexusBot"""
    
    def __init__(self):
        """Inicializa o cliente OpenAI"""
        self.api_key = os.getenv('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY não configurada")
            OPENAI_AVAILABLE = False
        else:
            openai.api_key = self.api_key
        
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7
        self.max_tokens = 500
        
    def get_system_prompt(self, user_profile=None):
        """Cria o prompt do sistema com contexto do usuário"""
        
        base_prompt = """Você é o NexusBot, um assistente inteligente da plataforma NexusLife.
        
        A NexusLife é uma plataforma de marketplace de serviços freelancer que conecta:
        - Pessoa Física (PF): Freelancers que oferecem serviços digitais
        - Pessoa Jurídica (PJ): Empresas que contratam freelancers
        
        Você deve:
        1. Ser amigável, profissional e prestativo
        2. Responder em português brasileiro
        3. Fornecer respostas úteis sobre a plataforma
        4. Ajudar com cadastro, contratos, pagamentos, avaliações
        5. Manter contexto das conversas anteriores
        6. Ser conciso nas respostas (máximo 300 palavras)
        7. Mencionar recursos específicos quando apropriado
        """
        
        # Adiciona contexto do usuário se disponível
        if user_profile:
            user_context = f"""
        
        Contexto do usuário:
        - Tipo de conta: {user_profile.get('person_type', 'Não definido')}
        - Avaliação: {user_profile.get('average_rating', 0)}/5.0 ⭐
        - Taxa de conclusão: {user_profile.get('completion_rate', 0)}%
        - Ganhos: R$ {user_profile.get('total_earnings', 0):.2f}
        
        Personalize suas respostas baseado no tipo de conta do usuário.
            """
            base_prompt += user_context
        
        return base_prompt
    
    def process_message(self, message, conversation_history=None, user_profile=None):
        """
        Processa uma mensagem e retorna a resposta do ChatGPT
        
        Args:
            message: Mensagem do usuário
            conversation_history: Lista de mensagens anteriores
            user_profile: Perfil do usuário para contexto
            
        Returns:
            dict: {
                'response': str (resposta do bot),
                'tokens_used': int (tokens consumidos),
                'error': str (erro se houver)
            }
        """
        
        if not OPENAI_AVAILABLE or not self.api_key:
            return {
                'response': None,
                'tokens_used': 0,
                'error': 'OpenAI não está disponível'
            }
        
        try:
            # Construir histórico de mensagens
            messages = [
                {"role": "system", "content": self.get_system_prompt(user_profile)}
            ]
            
            # Adicionar histórico de conversa
            if conversation_history:
                for msg in conversation_history:
                    messages.append({
                        "role": msg.get('role', 'user'),
                        "content": msg.get('content', '')
                    })
            
            # Adicionar mensagem atual
            messages.append({"role": "user", "content": message})
            
            # Chamar API OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            
            # Extrair resposta
            bot_response = response.choices[0].message.content.strip()
            tokens_used = response.usage.total_tokens
            
            logger.info(f"OpenAI response generated. Tokens: {tokens_used}")
            
            return {
                'response': bot_response,
                'tokens_used': tokens_used,
                'error': None
            }
            
        except openai.error.AuthenticationError as e:
            error_msg = "Erro de autenticação com OpenAI"
            logger.error(f"{error_msg}: {str(e)}")
            return {'response': None, 'tokens_used': 0, 'error': error_msg}
            
        except openai.error.RateLimitError as e:
            error_msg = "Limite de requisições OpenAI excedido. Tente novamente em alguns minutos."
            logger.error(f"{error_msg}: {str(e)}")
            return {'response': None, 'tokens_used': 0, 'error': error_msg}
            
        except openai.error.APIError as e:
            error_msg = f"Erro da API OpenAI: {str(e)}"
            logger.error(error_msg)
            return {'response': None, 'tokens_used': 0, 'error': error_msg}
            
        except Exception as e:
            error_msg = f"Erro ao processar mensagem: {str(e)}"
            logger.error(error_msg)
            return {'response': None, 'tokens_used': 0, 'error': error_msg}
    
    def generate_conversation_title(self, first_message):
        """Gera um título para a conversa baseado na primeira mensagem"""
        
        if not OPENAI_AVAILABLE or not self.api_key:
            return first_message[:50]
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Gere um título curto (máximo 5 palavras) em português para um tópico de conversa. Responda APENAS com o título, sem aspas."
                    },
                    {"role": "user", "content": first_message}
                ],
                temperature=0.5,
                max_tokens=20
            )
            
            title = response.choices[0].message.content.strip()
            return title if title else first_message[:50]
            
        except Exception as e:
            logger.warning(f"Erro ao gerar título: {str(e)}")
            return first_message[:50]


# Instância global
nexus_bot_ai = NexusBotAI() if OPENAI_AVAILABLE else None
