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
from .openai_integration import nexus_bot_ai, OPENAI_AVAILABLE
from .gemini_integration import gemini_bot_ai, GEMINI_AVAILABLE
from .chatbot import get_chatbot_response

logger = logging.getLogger(__name__)


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
        'ai_enabled': bool(OPENAI_AVAILABLE and nexus_bot_ai),
    }
    return render(request, 'core/chatbot.html', context)
