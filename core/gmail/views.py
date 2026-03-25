from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_http_methods
from .models import GmailToken
from .services import GmailService
import logging
import jwt
import json
import requests
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["GET"])
def initiate_auth(request):
    """Inicia fluxo OAuth"""
    try:
        # Parâmetros do OAuth 2.0
        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': settings.GMAIL_REDIRECT_URI,
            'response_type': 'code',
            'scope': ' '.join(settings.GMAIL_SCOPES),
            'access_type': 'offline',
            'prompt': 'consent',
        }
        
        authorization_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params)
        
        logger.info(f"OAuth flow initiated for user {request.user.username}")
        logger.info(f"Authorization URL: {authorization_url}")
        
        return redirect(authorization_url)
        
    except Exception as e:
        logger.error(f"Erro ao iniciar auth: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def oauth_callback(request):
    """Callback do OAuth"""
    try:
        code = request.GET.get('code')
        error = request.GET.get('error')
        
        if error:
            logger.error(f"OAuth error: {error}")
            return JsonResponse({
                'success': False,
                'error': f'OAuth error: {error}'
            }, status=400)
        
        if not code:
            logger.error("No authorization code provided")
            return JsonResponse({
                'success': False,
                'error': 'Código não fornecido'
            }, status=400)
        
        # Troca o código por um token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GMAIL_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        token_response = response.json()
        
        access_token = token_response.get('access_token')
        refresh_token = token_response.get('refresh_token')
        expires_in = token_response.get('expires_in')
        id_token = token_response.get('id_token')
        
        # Decodifica o ID token para obter o email
        email = None
        if id_token:
            decoded = jwt.decode(id_token, options={"verify_signature": False})
            email = decoded.get('email')
        
        # Calcula o tempo de expiração
        from datetime import datetime, timedelta
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in) if expires_in else None
        
        # Salva o token no banco de dados
        token, created = GmailToken.objects.update_or_create(
            user=request.user,
            defaults={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': expires_at,
                'email': email or '',
                'is_active': True,
            }
        )
        
        logger.info(f"Gmail token saved for user {request.user.username}, email: {email}")
        
        # Redireciona de volta para o perfil após conectar
        return redirect('profile')
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao trocar código por token: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Erro ao obter token: {str(e)}'
        }, status=500)
    except Exception as e:
        logger.error(f"Erro no callback: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def connection_status(request):
    """Verifica status da conexão"""
    try:
        token = GmailToken.objects.filter(user=request.user, is_active=True).first()
        
        if not token:
            return JsonResponse({
                'connected': False,
                'message': 'Gmail não conectado'
            })
        
        service = GmailService(request.user)
        test_result = service.test_connection()
        
        return JsonResponse({
            'connected': True,
            'email': token.email,
            'expires_at': token.expires_at,
            'profile': test_result
        })
        
    except Exception as e:
        return JsonResponse({
            'connected': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_emails(request):
    """Obtém emails do Gmail"""
    try:
        service = GmailService(request.user)
        emails = service.get_unread_messages(max_results=10)
        
        return JsonResponse({
            'success': True,
            'emails': emails
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
