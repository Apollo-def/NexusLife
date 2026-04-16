import logging
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth as firebase_admin_auth

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'firebase-credentials.json')

firebase_admin_initialized = False

def initialize_firebase_admin():
    global firebase_admin_initialized
    
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            firebase_admin_initialized = True
            logger.info("Firebase Admin SDK inicializado com sucesso!")
        except FileNotFoundError:
            logger.warning(f"Arquivo de credenciais do Firebase não encontrado em: {FIREBASE_CREDENTIALS_PATH}. Firebase Admin desabilitado. Para habilitar, siga as instruções no README.md.")
            firebase_admin_initialized = False
        except Exception as e:
            logger.warning(f"Firebase Admin não pôde ser inicializado: {e}. Firebase Admin desabilitado. O servidor continuará funcionando.")
            firebase_admin_initialized = False
    else:
        firebase_admin_initialized = True
    
    return firebase_admin_initialized

firebase_config = {
    "apiKey": "AIzaSyA1EvjdlY3OWUc5KoR70O9r81MkNNCmec4",
    "authDomain": "nexuslife-1409b.firebaseapp.com",
    "projectId": "nexuslife-1409b",
    "storageBucket": "nexuslife-1409b.firebasestorage.app",
    "messagingSenderId": "162871176799",
    "appId": "1:162871176799:web:5ddc2cc315a5c2f98075ea",
    "measurementId": "G-D54PLMVJH7"
}

def verify_firebase_token(id_token):
    if not firebase_admin_initialized:
        logger.warning("Firebase Admin não está inicializado. Não é possível verificar tokens.")
        return None
    
    try:
        decoded_token = firebase_admin_auth.verify_id_token(id_token)
        return decoded_token
    except firebase_admin_auth.InvalidIdTokenError:
        return None
    except firebase_admin_auth.ExpiredIdTokenError:
        return None
    except Exception as e:
        logger.error(f"Erro ao verificar token: {e}")
        return None

