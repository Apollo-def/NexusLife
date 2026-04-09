import logging
import os
from django.conf import settings
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth as firebase_admin_auth
import pyrebase

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
            logger.warning(f"Arquivo de credenciais do Firebase não encontrado em: {FIREBASE_CREDENTIALS_PATH}. Firebase Admin desabilitado. Para habilitar, siga as instruções no README.md. O servidor continuará funcionando com Pyrebase para autenticação básica.")
            firebase_admin_initialized = False
        except Exception as e:
            logger.warning(f"Firebase Admin não pôde ser inicializado: {e}. Firebase Admin desabilitado. O servidor continuará funcionando.")
            firebase_admin_initialized = False
    else:
        firebase_admin_initialized = True
    
    return firebase_admin_initialized

# Firebase configuration for Pyrebase (Python SDK)
firebase_config = {
    "apiKey": settings.FIREBASE_CONFIG.get('apiKey'),
    "authDomain": settings.FIREBASE_CONFIG.get('authDomain'),
    "projectId": settings.FIREBASE_CONFIG.get('projectId'),
    "storageBucket": settings.FIREBASE_CONFIG.get('storageBucket'),
    "messagingSenderId": settings.FIREBASE_CONFIG.get('messagingSenderId'),
    "appId": settings.FIREBASE_CONFIG.get('appId'),
    "databaseURL": "",
    "measurementId": settings.FIREBASE_CONFIG.get('measurementId')
}

logger.info(f"Firebase configurado para projeto: {firebase_config.get('projectId')}")

firebase = pyrebase.initialize_app(firebase_config)
auth_firebase = firebase.auth()

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

