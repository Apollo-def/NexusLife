from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from .models import GmailToken
import logging

logger = logging.getLogger(__name__)


class GmailService:
    """Serviço para interagir com Gmail API"""
    
    def __init__(self, user):
        self.user = user
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Autentica e cria o serviço do Gmail"""
        try:
            token_obj = GmailToken.objects.get(user=self.user, is_active=True)
            
            credentials = Credentials(
                token=token_obj.access_token,
                refresh_token=token_obj.refresh_token,
                token_uri='https://oauth2.googleapis.com/token',
                client_id='562969126249-7h8jhi6r0f8hfas2srfje52bm5o3f0ki.apps.googleusercontent.com',
                client_secret='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'
            )
            
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            
            self.service = build('gmail', 'v1', credentials=credentials)
        except GmailToken.DoesNotExist:
            logger.error(f"Token não encontrado para usuário {self.user}")
            raise Exception("Gmail não conectado")
    
    def test_connection(self):
        """Testa a conexão com Gmail"""
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            return {
                'email': profile.get('emailAddress'),
                'messages_total': profile.get('messagesTotal'),
                'threads_total': profile.get('threadsTotal')
            }
        except Exception as e:
            logger.error(f"Erro ao testar conexão: {e}")
            raise
    
    def get_unread_messages(self, max_results=10):
        """Obtém mensagens não lidas"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            email_list = []
            
            for msg in messages:
                msg_data = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                
                headers = msg_data['payload']['headers']
                email_list.append({
                    'id': msg['id'],
                    'from': next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown'),
                    'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject'),
                    'date': next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown'),
                })
            
            return email_list
        except Exception as e:
            logger.error(f"Erro ao obter mensagens: {e}")
            raise
    
    def send_email(self, to, subject, body):
        """Envia um e-mail"""
        try:
            from email.mime.text import MIMEText
            import base64
            
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail: {e}")
            raise
