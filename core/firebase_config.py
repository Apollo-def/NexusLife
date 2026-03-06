import os # Módulo para interagir com o sistema operacional, usado para construir caminhos de arquivo.
import firebase_admin # SDK do Firebase para Python (operações de back-end).
from firebase_admin import credentials # Para manusear as credenciais de serviço do Firebase.
from firebase_admin import auth as firebase_admin_auth # Módulo de autenticação do Firebase Admin.
import pyrebase # Biblioteca cliente para interagir com serviços Firebase (como autenticação no lado do cliente).

# Caminho para o arquivo de credenciais do Firebase
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Pega o diretório raiz do projeto (NexusLife/).
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'firebase-credentials.json') # Constrói o caminho completo para o arquivo de credenciais.

# Flag para verificar se Firebase Admin foi inicializado
firebase_admin_initialized = False

# Configuração do Firebase Admin (para operações no servidor)
def initialize_firebase_admin():
    """
    Inicializa o Firebase Admin SDK.
    Esta função garante que o SDK seja inicializado apenas uma vez.
    """
    global firebase_admin_initialized
    
    if not firebase_admin._apps: # Verifica se o app do Firebase já foi inicializado para evitar erros.
        try:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            firebase_admin_initialized = True
            print("Firebase Admin SDK inicializado com sucesso!")
        except FileNotFoundError:
            print(
                f"AVISO: Arquivo de credenciais do Firebase não encontrado em: {FIREBASE_CREDENTIALS_PATH}\n"
                "Firebase Admin será desabilitado. Para habilitar, siga as instruções no README.md.\n"
                "O servidor continuará funcionando com Pyrebase para autenticação básica."
            )
            firebase_admin_initialized = False
        except Exception as e:
            print(
                f"AVISO: Firebase Admin não pôde ser inicializado: {e}\n"
                "Firebase Admin será desabilitado. O servidor continuará funcionando."
            )
            firebase_admin_initialized = False
    else:
        firebase_admin_initialized = True
    
    return firebase_admin_initialized # Retorna True se foi inicializado, False caso contrário.

# Configuração do Pyrebase (para autenticação no cliente)
# Você precisa obter estas configurações no console do Firebase
# Vá para: Configurações do projeto > Geral > Seus apps > Web app (</>)
firebase_config = {
    "apiKey": "AIzaSyA1EvjdlY3OWUc5KoR70O9r81MkNNCmec4", # Chave de API para autorizar requisições.
    "authDomain": "nexuslife-1409b.firebaseapp.com", # Domínio de autenticação do seu projeto.
    "projectId": "nexuslife-1409b", # ID do seu projeto Firebase.
    "storageBucket": "nexuslife-1409b.firebasestorage.app", # Bucket do Cloud Storage.
    "messagingSenderId": "162871176799", # ID para o serviço de mensageria (FCM).
    "appId": "1:162871176799:web:4eac3ea69282d4838075ea", # ID do seu aplicativo web no Firebase.
    "databaseURL": "", # URL do Realtime Database (opcional se não estiver usando).
    "measurementId": "G-PZSRLEY1W6" # ID do Google Analytics.
}

# Inicializar Pyrebase
firebase = pyrebase.initialize_app(firebase_config) # Inicializa a biblioteca Pyrebase com as configurações acima.
auth_firebase = firebase.auth() # Cria um objeto de autenticação para interagir com o Firebase Auth (ex: criar usuário, fazer login).

# Função helper para verificar token JWT
def verify_firebase_token(id_token):
    """
    Verifica um token JWT do Firebase e retorna os dados do usuário.
    Usa o Firebase Admin SDK, que deve ser executado no servidor.
    """
    if not firebase_admin_initialized:
        print("Firebase Admin não está inicializado. Não é possível verificar tokens.")
        return None
    
    try:
        # Usa o SDK Admin para verificar a validade e a assinatura do token.
        decoded_token = firebase_admin_auth.verify_id_token(id_token)
        return decoded_token # Retorna os dados decodificados do usuário (uid, email, etc.).
    except firebase_admin_auth.InvalidIdTokenError:
        return None # O token é inválido (malformado, assinatura errada, etc.).
    except firebase_admin_auth.ExpiredIdTokenError:
        return None # O token expirou.
    except Exception as e:
        print(f"Erro ao verificar token: {e}")
        return None # Outros erros.

