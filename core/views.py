from django.shortcuts import render, redirect # Funções para renderizar templates e redirecionar URLs.
from django.contrib.auth import login, authenticate, logout # Funções de autenticação do Django.
from django.contrib.auth.models import User # Modelo de usuário do Django.
from django.contrib import messages # Framework de mensagens para exibir notificações ao usuário.
from django.contrib.auth.decorators import login_required # Decorator para proteger views, exigindo que o usuário esteja logado.
from .forms import UserRegisterForm, LoginForm, UserUpdateForm # Importa os formulários definidos em forms.py.
from .firebase_config import auth_firebase, initialize_firebase_admin # Objeto de autenticação do Pyrebase e função de inicialização.
from firebase_admin import firestore # Para interagir com o banco de dados Firestore.
from requests.exceptions import HTTPError # Para capturar erros de requisição do Firebase.
import json # Para analisar as respostas de erro do Firebase.

# Inicializa o Firebase Admin ao importar o módulo
try:
    initialize_firebase_admin()
except Exception as e:
    print(f"Aviso: Firebase Admin não pôde ser inicializado: {e}")

def login_view(request):
    """
    View para a página de login.
    """
    if request.method == 'POST': # Se o formulário foi enviado (requisição POST).
        form = LoginForm(request.POST) # Cria uma instância do formulário com os dados enviados.
        if form.is_valid(): # Verifica se os dados do formulário são válidos.
            username = form.cleaned_data['username'].strip() # Pega o nome de usuário limpo.
            password = form.cleaned_data['password'] # Pega a senha limpa.
            
            # Tenta autenticar com o nome de usuário exato
            user = authenticate(request, username=username, password=password)
            
            # Se não encontrou, tenta com lowercase (para兼容com registros antigos)
            if user is None:
                user = authenticate(request, username=username.lower(), password=password)
            
            # Se ainda não encontrou, verifica se é email e busca pelo email
            if user is None and '@' in username:
                try:
                    django_user = User.objects.get(email=username)
                    user = authenticate(request, username=django_user.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None: # Se a autenticação for bem-sucedida.
                login(request, user) # Inicia a sessão para o usuário.
                messages.success(request, f'Bem-vindo, {user.first_name or user.username}!') # Exibe uma mensagem de sucesso.
                return redirect('home') # Redireciona para a página 'home'.
            else:
                messages.error(request, 'Usuário ou senha inválidos.') # Se a autenticação falhar, exibe uma mensagem de erro.
    else:
        form = LoginForm() # Se for uma requisição GET, cria um formulário em branco.
    
    return render(request, 'core/login.html', {'form': form}) # Renderiza o template de login com o formulário.


def register_view(request):
    """
    View para a página de registro. Cria o usuário no Firebase e no Django.
    """
    if request.method == 'POST': # Se o formulário de registro foi enviado.
        form = UserRegisterForm(request.POST) # Cria uma instância do formulário com os dados enviados.
        if form.is_valid(): # Verifica se os dados são válidos.
            # Pega os dados limpos do formulário
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2') # O form já valida se password1 e password2 são iguais.
            cpf = form.cleaned_data.get('cpf')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            try:
                # 1. Tenta criar o usuário no Firebase Authentication
                user_firebase = auth_firebase.create_user_with_email_and_password(email, password)
                uid = user_firebase['localId']

                # 2. Se o usuário foi criado no Firebase, cria no Django também
                user_django = form.save(commit=False)
                user_django.username = username.lower()
                user_django.save()

                # 3. Salva os dados adicionais (CPF, etc.) no Firestore
                db = firestore.client()
                user_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'cpf': cpf
                }
                db.collection('users').document(uid).set(user_data)

                # 4. (Opcional) Envia um e-mail de verificação para o usuário
                auth_firebase.send_email_verification(user_firebase['idToken'])

                messages.success(request, f'Conta criada para {username}! Um e-mail de verificação foi enviado. Por favor, verifique sua caixa de entrada.')
                return redirect('login')

            except HTTPError as e:
                # Captura e trata erros específicos do Firebase
                error_json = e.args[1]
                error_data = json.loads(error_json)
                error_message = error_data['error']['message']
                
                if 'EMAIL_EXISTS' in error_message:
                    messages.error(request, 'Este endereço de e-mail já está em uso.')
                elif 'WEAK_PASSWORD' in error_message:
                    messages.error(request, 'A senha é muito fraca. Use pelo menos 6 caracteres.')
                else:
                    messages.error(request, f'Ocorreu um erro durante o registro: {error_message}')
            
            except Exception as e:
                # Captura outros erros inesperados
                messages.error(request, f'Ocorreu um erro inesperado: {e}')
    else:
        form = UserRegisterForm() # Se for uma requisição GET, cria um formulário de registro em branco.
    
    return render(request, 'core/register.html', {'form': form}) # Renderiza o template de registro com o formulário.


@login_required
def profile_view(request):
    """
    View para a página de perfil do usuário, permitindo a edição de dados.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Seu perfil foi atualizado com sucesso!')
                return redirect('profile')
            except Exception as e:
                messages.error(request, f'Erro ao salvar perfil: {e}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'core/profile.html', context)


@login_required # Este decorator garante que apenas usuários logados possam acessar esta view.
def home_view(request):
    return render(request, 'core/home.html') # Renderiza a página inicial do usuário logado.


def logout_view(request):
    logout(request) # Encerra a sessão do usuário atual.
    messages.info(request, 'Você foi desconectado.') # Exibe uma mensagem informativa.
    return redirect('login') # Redireciona o usuário para a página de login.
