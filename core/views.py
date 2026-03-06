from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LoginForm, UserUpdateForm
from .firebase_config import auth_firebase, initialize_firebase_admin, firebase_admin_initialized

if firebase_admin_initialized:
    from firebase_admin import firestore
from requests.exceptions import HTTPError
import json

try:
    initialize_firebase_admin()
except Exception as e:
    print(f"Aviso: Firebase Admin não pôde ser inicializado: {e}")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                user = authenticate(request, username=username.lower(), password=password)
            
            if user is None and '@' in username:
                try:
                    django_user = User.objects.get(email=username)
                    user = authenticate(request, username=django_user.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            cpf = form.cleaned_data.get('cpf')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            try:
                user_firebase = auth_firebase.create_user_with_email_and_password(email, password)
                uid = user_firebase['localId']

                user_django = form.save(commit=False)
                user_django.username = username.lower()
                user_django.save()

                if firebase_admin_initialized:
                    db = firestore.client()
                    user_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'cpf': cpf
                    }
                    db.collection('users').document(uid).set(user_data)

                auth_firebase.send_email_verification(user_firebase['idToken'])

                messages.success(request, f'Conta criada para {username}! Um e-mail de verificação foi enviado.')
                return redirect('login')

            except HTTPError as e:
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
                messages.error(request, f'Ocorreu um erro inesperado: {e}')
    else:
        form = UserRegisterForm()
    
    return render(request, 'core/register.html', {'form': form})


@login_required
def profile_view(request):
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


@login_required
def home_view(request):
    return render(request, 'core/home.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Você foi desconectado.')
    return redirect('login')


def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, 'Por favor, insira seu endereço de email.')
            return render(request, 'core/password_reset.html')
        
        try:
            auth_firebase.send_password_reset_email(email)
            messages.success(request, f'Um email de redefinição de senha foi enviado para {email}. Verifique sua caixa de entrada.')
            return redirect('login')
        except HTTPError as e:
            try:
                error_json = e.args[1]
                error_data = json.loads(error_json)
                error_message = error_data['error']['message']
                
                if 'EMAIL_NOT_FOUND' in error_message:
                    messages.error(request, 'Este email não está cadastrado em nosso sistema.')
                else:
                    messages.error(request, f'Ocorreu um erro ao enviar o email de redefinição: {error_message}')
            except:
                messages.error(request, 'Ocorreu um erro ao processar sua solicitação. Tente novamente.')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro inesperado: {e}')
    
    return render(request, 'core/password_reset.html')

