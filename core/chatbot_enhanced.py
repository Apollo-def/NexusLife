"""
Chatbot Melhorado com Gemini AI Integration
Provides enhanced AI responses with conversation memory and fallback
"""

import uuid
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import ChatbotConversation, ChatbotMessage, UserProfile
# Removed unused OpenAI integration
from .gemini_integration import gemini_bot_ai, GEMINI_AVAILABLE
# from .chatbot import get_chatbot_response  # Removed - now defined locally

logger = logging.getLogger(__name__)

# Configurações do chatbot
CHATBOT_CONFIG = {
    'name': 'NexusBot',
    'version': '1.0',
    'responses': {
        'oi': ['Olá! Sou o NexusBot, assistente do NexusLife! Como posso ajudar você hoje?', 'Oi! Bem-vindo ao NexusLife! O que você precisa?'],
        'ola': ['Olá! Sou o NexusBot, assistente do NexusLife! Como posso ajudar você hoje?', 'Oi! Bem-vindo ao NexusLife! O que você precisa?'],
        'bom dia': ['Bom dia! <i class="fas fa-sun"></i> Como posso ajudar você no NexusLife hoje?', 'Bom dia! O NexusLife está aqui para ajudar!'],
        'boa tarde': ['Boa tarde! <i class="fas fa-cloud-sun"></i> Como posso auxiliar você na nossa plataforma?', 'Boa tarde! Pronto para ajudar com o NexusLife!'],
        'boa noite': ['Boa noite! <i class="fas fa-moon"></i> Como posso ajudar você agora?', 'Boa noite! O NexusLife nunca dorme para ajudar você!'],
        'ajuda': ['Estou aqui para ajudar! Você pode perguntar sobre:\n• Como se cadastrar (PF/PJ)\n• Como contratar serviços\n• Como oferecer serviços\n• Como usar o marketplace\n• Problemas com conta\n• Sistema de avaliações\n• Dashboards PF/PJ'],
        'cadastro': ['Para se cadastrar no NexusLife:\n1. Clique em "Registrar" no menu\n2. Escolha PF (Pessoa Física) ou PJ (Pessoa Jurídica)\n3. Preencha seus dados pessoais\n4. Para PJ: inclua inscrição estadual\n5. Verifique seu e-mail\n6. Complete seu perfil no dashboard'],
        'pf': ['Pessoa Física no NexusLife:\n• Perfil para freelancers individuais\n• Ofereça serviços como designer, programador, etc.\n• Dashboard simplificado em /marketplace/dashboard/pf/\n• Gerencie seus serviços e pedidos\n• Receba avaliações dos clientes'],
        'pj': ['Pessoa Jurídica no NexusLife:\n• Perfil para empresas/agências\n• Contrate freelancers para projetos\n• Dashboard completo em /marketplace/dashboard/pj/\n• Gerencie múltiplos pedidos\n• Avalie freelancers contratados'],
        'servicos': ['Para contratar serviços no NexusLife:\n1. Faça login como PJ\n2. Vá para "Marketplace" no menu\n3. Navegue pelos serviços disponíveis\n4. Use filtros por categoria/preço\n5. Clique em "Contratar" no serviço desejado\n6. Preencha detalhes do pedido\n7. Acompanhe no seu dashboard'],
        'freelancer': ['Para oferecer serviços como freelancer:\n1. Cadastre-se como PF (Pessoa Física)\n2. Complete seu perfil em /profile/\n3. Adicione suas habilidades e experiência\n4. Crie serviços em /marketplace/service/create/\n5. Defina preços e descrições\n6. Receba pedidos no dashboard\n7. Entregue trabalhos e receba avaliações'],
        'marketplace': ['O Marketplace NexusLife oferece:\n• Serviços digitais diversos\n• Filtros por categoria e preço\n• Perfis de freelancers verificados\n• Sistema de avaliações\n• Pedidos seguros\n• Dashboards separados PF/PJ\n• Favoritos para salvar serviços'],
        'dashboard': ['Dashboards NexusLife:\n\nPara PF (Freelancer):\n• /marketplace/dashboard/pf/\n• Meus serviços oferecidos\n• Pedidos recebidos\n• Avaliações recebidas\n\nPara PJ (Cliente):\n• /marketplace/dashboard/pj/\n• Serviços contratados\n• Pedidos em andamento\n• Histórico de compras'],
        'avaliacao': ['Sistema de avaliações NexusLife:\n• Clientes avaliam freelancers (1-5 estrelas)\n• Comentários sobre qualidade do trabalho\n• Avaliações aparecem nos perfis\n• Média calculada automaticamente\n• Ajuda outros usuários na escolha\n• Freelancers podem responder comentários'],
        'favoritos': ['Sistema de Favoritos:\n• Salve serviços que interessam\n• Acesse rapidamente depois\n• Compare preços e avaliações\n• Organize seus interesses\n• Receba notificações (futuro)\n• Lista pessoal no seu perfil'],
        'pedido': ['Como funciona um pedido:\n1. Cliente contrata serviço\n2. Freelancer recebe notificação\n3. Combinam detalhes e prazo\n4. Freelancer executa trabalho\n5. Entrega final\n6. Cliente aprova e paga\n7. Avaliação é feita\n8. Reputação aumenta'],
        'problema': ['Problemas comuns e soluções:\n\nLogin/Registro:\n• Verifique email e senha\n• Use "Esqueci senha" se necessário\n• Limpe cache do navegador\n\nPedidos:\n• Verifique status no dashboard\n• Contate freelancer diretamente\n• Use suporte se necessário\n\nPerfil:\n• Complete todas informações\n• Adicione foto profissional\n• Verifique dados PF/PJ'],
        'contato': ['Para suporte no NexusLife:\n• Use este chatbot 24/7\n• Acesse "Ajuda" no seu dashboard\n• Consulte a documentação em README.md\n• Para questões urgentes: verifique seu painel de controle\n• Relate problemas através do sistema de suporte integrado'],
        'preco': ['Precificação no NexusLife:\n\nPara Freelancers (PF):\n• Defina seus próprios preços\n• Crie pacotes (básico/premium)\n• Negocie diretamente com clientes\n\nPara Clientes (PJ):\n• Compare preços de diferentes freelancers\n• Pacotes ajudam a escolher o ideal\n• Pagamento seguro garantido\n• Sem taxas ocultas na contratação'],
        'seguranca': ['Segurança no NexusLife:\n• Plataforma segura para freelancers e clientes\n• Pagamentos protegidos\n• Verificação de perfis de usuários\n• Sistema de avaliações para confiança\n• Suporte para resolução de disputas\n• Dados pessoais criptografados\n• Ambiente confiável para negócios digitais'],
        'default': ['Desculpe, não entendi sua pergunta sobre o NexusLife. Tente:\n• "ajuda" - ver todas opções\n• "cadastro" - como se registrar\n• "servicos" - contratar freelancers\n• "freelancer" - oferecer serviços\n• "dashboard" - gerenciar conta\n• Ou reformule sua pergunta!']
    }
}

def get_chatbot_response(message):
    """Processa a mensagem e retorna uma resposta apropriada"""
    if not message:
        return "Por favor, digite uma mensagem."

    message = message.lower().strip()

    # Verificar correspondências exatas
    for key, responses in CHATBOT_CONFIG['responses'].items():
        if key in message:
            return responses[0] if isinstance(responses, list) else responses

    # Verificar palavras-chave parciais
    keywords = {
        'cadastro': 'cadastro',
        'registrar': 'cadastro',
        'conta': 'cadastro',
        'login': 'cadastro',
        'cadastrar': 'cadastro',
        'pf': 'pf',
        'pessoa fisica': 'pf',
        'freelancer': 'freelancer',
        'trabalhar': 'freelancer',
        'oferecer': 'freelancer',
        'pj': 'pj',
        'pessoa juridica': 'pj',
        'empresa': 'pj',
        'cliente': 'pj',
        'contratar': 'servicos',
        'servico': 'servicos',
        'serviços': 'servicos',
        'contratar': 'servicos',
        'marketplace': 'marketplace',
        'plataforma': 'marketplace',
        'dashboard': 'dashboard',
        'painel': 'dashboard',
        'avaliacao': 'avaliacao',
        'avaliação': 'avaliacao',
        'avaliações': 'avaliacao',
        'avaliacoes': 'avaliacao',
        'review': 'avaliacao',
        'estrelas': 'avaliacao',
        'favoritos': 'favoritos',
        'favorito': 'favoritos',
        'salvar': 'favoritos',
        'pedido': 'pedido',
        'ordem': 'pedido',
        'projeto': 'pedido',
        'problema': 'problema',
        'erro': 'problema',
        'nao funciona': 'problema',
        'bug': 'problema',
        'contato': 'contato',
        'suporte': 'contato',
        'ajuda': 'contato',
        'preco': 'preco',
        'preço': 'preco',
        'preços': 'preco',
        'precos': 'preco',
        'custa': 'preco',
        'valor': 'preco',
        'custo': 'preco',
        'seguranca': 'seguranca',
        'segurança': 'seguranca',
        'seguro': 'seguranca',
        'protegido': 'seguranca'
    }

    for keyword, response_key in keywords.items():
        if keyword in message:
            responses = CHATBOT_CONFIG['responses'][response_key]
            return responses[0] if isinstance(responses, list) else responses

    # Resposta padrão
    return CHATBOT_CONFIG['responses']['default'][0]


def get_user_profile_context(user):
    """Extrai contexto do perfil do usuário"""
    try:
        profile = UserProfile.objects.get(user=user)
        return {
            'person_type': profile.get_person_type_display() if profile.person_type else 'Não definido',
            'average_rating': float(profile.average_rating or 0),
            'completion_rate': float(profile.completion_rate or 0),
            'total_earnings': float(profile.total_earnings or 0),
        }
    except UserProfile.DoesNotExist:
        return None


@csrf_exempt
@require_http_methods(["POST"])
def chatbot_api(request):
    """
    API endpoint para o chatbot com OpenAI
    POST /api/chatbot/
    
    Body:
    {
        "message": "sua mensagem",
        "session_id": "session_uuid (opcional)",
        "use_ai": true/false (opcional, padrão: true)
    }
    """
    
    try:
        import json
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        session_id = data.get('session_id', '')
        use_ai = data.get('use_ai', True)
        
        if not message:
            return JsonResponse({'error': 'Mensagem vazia'}, status=400)
        
        # Gerar session_id se não fornecido
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Obter ou criar conversa
        user = getattr(request, 'user', None)
        if user and hasattr(user, 'is_authenticated') and not user.is_authenticated:
            user = None
        conversation, created = ChatbotConversation.objects.get_or_create(
            session_id=session_id,
            defaults={'user': user}
        )
        
        # Salvar mensagem do usuário
        user_message = ChatbotMessage.objects.create(
            conversation=conversation,
            sender='user',
            message=message
        )
        
        # Obter histórico de conversas (últimas 10 mensagens)
        history_messages = list(ChatbotMessage.objects.filter(
            conversation=conversation
        ).order_by('created_at')[:10])
        
        conversation_history = [
            {
                'role': 'user' if msg.sender == 'user' else 'assistant',
                'content': msg.message
            }
            for msg in history_messages
        ]
        
        # Escolher modo de resposta
        bot_response = None
        tokens_used = 0
        
        # Tentar usar Gemini AI primeiro
        if GEMINI_AVAILABLE and gemini_bot_ai:
            try:
                user_profile = get_user_profile_context(user) if user else None
                gemini_response = gemini_bot_ai.process_message(
                    message=message,
                    conversation_history=conversation_history,
                    user_profile=user_profile
                )
                
                if gemini_response.get('response') and not gemini_response.get('error'):
                    bot_response = gemini_response['response']
                    logger.info(f"Resposta gerada com Gemini AI para: {message[:50]}")
                else:
                    logger.warning(f"Gemini AI retornou erro: {gemini_response.get('error')}")
                    
            except Exception as e:
                logger.error(f"Erro ao usar Gemini AI: {str(e)}")
        
        # Fallback para respostas baseadas em dicionário se Gemini falhar
        if not bot_response:
            bot_response = get_chatbot_response(message)
            logger.info(f"Usando resposta do dicionário para: {message[:50]}")
        
        # Salvar resposta do bot
        bot_message = ChatbotMessage.objects.create(
            conversation=conversation,
            sender='bot',
            message=bot_response,
            tokens_used=tokens_used
        )
        
        # Atualizar título da conversa se for a primeira mensagem
        if created:
            try:
                title = message[:50]  # Usa primeiros 50 caracteres como título
                conversation.title = title
                conversation.save()
            except Exception as e:
                logger.warning(f"Erro ao gerar título: {str(e)}")
        
        return JsonResponse({
            'session_id': session_id,
            'message': bot_response,
            'response': bot_response,
            'bot_name': 'NexusBot',
            'tokens_used': tokens_used,
            'ai_enabled': bool(GEMINI_AVAILABLE and gemini_bot_ai),
            'ai_provider': 'Gemini' if (GEMINI_AVAILABLE and gemini_bot_ai) else 'Dictionary',
            'timestamp': timezone.now().isoformat()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        logger.error(f"Erro no chatbot API: {str(e)}")
        return JsonResponse({'error': 'Erro ao processar mensagem'}, status=500)


@login_required
def chatbot_conversations(request):
    """Listar conversas do usuário"""
    conversations = ChatbotConversation.objects.filter(user=request.user).prefetch_related('messages')
    
    context = {
        'conversations': conversations,
        'ai_enabled': bool(GEMINI_AVAILABLE and gemini_bot_ai),
        'ai_provider': 'Gemini' if (GEMINI_AVAILABLE and gemini_bot_ai) else 'Dictionary',
    }
    return render(request, 'core/chatbot_conversations.html', context)


@login_required
def chatbot_conversation_detail(request, session_id):
    """Detalhes de uma conversa específica"""
    try:
        conversation = ChatbotConversation.objects.get(session_id=session_id, user=request.user)
        messages = ChatbotMessage.objects.filter(conversation=conversation).order_by('created_at')
        
        context = {
            'conversation': conversation,
            'messages': messages,
            'session_id': session_id,
            'ai_enabled': bool(GEMINI_AVAILABLE and gemini_bot_ai),
            'ai_provider': 'Gemini' if (GEMINI_AVAILABLE and gemini_bot_ai) else 'Dictionary',
        }
        return render(request, 'core/chatbot_conversation_detail.html', context)
        
    except ChatbotConversation.DoesNotExist:
        return render(request, '404.html', status=404)


@login_required
def delete_conversation(request, session_id):
    """Deletar uma conversa"""
    try:
        conversation = ChatbotConversation.objects.get(session_id=session_id, user=request.user)
        conversation.delete()
        return JsonResponse({'success': True, 'message': 'Conversa deletada com sucesso'})
    except ChatbotConversation.DoesNotExist:
        return JsonResponse({'error': 'Conversa não encontrada'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao deletar conversa: {str(e)}")
        return JsonResponse({'error': 'Erro ao deletar conversa'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_conversation(request):
    """Obter histórico de conversa"""
    session_id = request.GET.get('session_id', '')
    
    if not session_id:
        return JsonResponse({'error': 'session_id não fornecido'}, status=400)
    
    try:
        conversation = ChatbotConversation.objects.get(session_id=session_id)
        messages = ChatbotMessage.objects.filter(conversation=conversation).order_by('created_at')
        
        message_list = [
            {
                'sender': msg.sender,
                'message': msg.message,
                'timestamp': msg.created_at.isoformat(),
                'tokens_used': msg.tokens_used
            }
            for msg in messages
        ]
        
        return JsonResponse({
            'session_id': session_id,
            'title': conversation.title,
            'messages': message_list,
            'message_count': len(message_list)
        })
        
    except ChatbotConversation.DoesNotExist:
        return JsonResponse({'error': 'Conversa não encontrada'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao obter conversa: {str(e)}")
        return JsonResponse({'error': 'Erro ao obter conversa'}, status=500)


def chatbot_view(request):
    """View para exibir a interface do chatbot"""
    context = {
        'ai_enabled': bool(GEMINI_AVAILABLE and gemini_bot_ai),
    }
    return render(request, 'core/chatbot.html', context)
