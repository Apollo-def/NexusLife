from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import logging
from .forms import UserRegisterForm, LoginForm, UserUpdateForm
from .models import UserProfile, Notification
from .firebase_config import auth_firebase, initialize_firebase_admin, firebase_admin_initialized

logger = logging.getLogger(__name__)

if firebase_admin_initialized:
    from firebase_admin import firestore
from requests.exceptions import HTTPError
import json

try:
    initialize_firebase_admin()
except Exception as e:
    logger.warning(f"Firebase Admin não pôde ser inicializado: {e}")

def _find_user_by_cpf(cpf_input):
    cpf_input = cpf_input.strip() if cpf_input else ''
    if not cpf_input:
        return None

    cpf_digits = ''.join(ch for ch in cpf_input if ch.isdigit())

    # Busca CPF local no perfil do usuário
    if cpf_digits:
        for profile in UserProfile.objects.all():
            profile_cpf = ''.join(ch for ch in (profile.cpf_cnpj or '') if ch.isdigit())
            if profile_cpf == cpf_digits:
                return profile.user

    if not firebase_admin_initialized:
        return None

    try:
        db = firestore.client()
        for cpf_candidate in (cpf_input, cpf_digits):
            if not cpf_candidate:
                continue
            query = db.collection('users').where('cpf', '==', cpf_candidate).stream()
            for doc in query:
                data = doc.to_dict() or {}
                email = data.get('email')
                if email:
                    try:
                        return User.objects.get(email__iexact=email.strip())
                    except User.DoesNotExist:
                        continue
    except Exception:
        pass

    return None


def _get_user_from_credential(credential):
    credential = (credential or '').strip()
    if not credential:
        return None

    try:
        user = User.objects.filter(username__iexact=credential).first()
        if user:
            return user

        user = User.objects.filter(email__iexact=credential).first()
        if user:
            return user

        # Busca CPF local no perfil do usuário
        cpf_digits = ''.join(ch for ch in credential if ch.isdigit())
        if cpf_digits:
            for profile in UserProfile.objects.all():
                profile_cpf = ''.join(ch for ch in (profile.cpf_cnpj or '') if ch.isdigit())
                if profile_cpf == cpf_digits:
                    return profile.user

        # Busca CPF no Firestore, se disponível
        if firebase_admin_initialized:
            db = firestore.client()
            for cpf_query in (credential, cpf_digits):
                if not cpf_query:
                    continue
                for doc in db.collection('users').where('cpf', '==', cpf_query).stream():
                    data = doc.to_dict() or {}
                    email = data.get('email')
                    if email:
                        try:
                            return User.objects.get(email__iexact=email.strip())
                        except User.DoesNotExist:
                            continue
    except Exception:
        pass

    return None


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            credential = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            # Tentar com Django primeiro
            user = authenticate(request, username=credential, password=password)
            if user is None and credential:
                user = authenticate(request, username=credential.lower(), password=password)

            # Se não encontrou com Django, buscar por CPF/email e tentar autenticar
            if user is None:
                possible_user = _get_user_from_credential(credential)
                if possible_user:
                    user = authenticate(request, username=possible_user.username, password=password)
                    if user is None:
                        # Tenta com Firebase se Django falhar
                        try:
                            firebase_user = auth_firebase.sign_in_with_email_and_password(possible_user.email, password)
                            # Se Firebase funciona, sincroniza a senha no Django
                            possible_user.set_password(password)
                            possible_user.save()
                            user = authenticate(request, username=possible_user.username, password=password)
                            logger.info(f"Sincronizou senha via Firebase para {possible_user.email}")
                        except Exception as fb_error:
                            logger.warning(f"Firebase login fail for {possible_user.email}: {fb_error}")
                            messages.error(request, 'Senha inválida. Por favor verifique e tente novamente.')
                else:
                    # Último recurso: tentar direto com Firebase usando email/CPF
                    try:
                        firebase_user = auth_firebase.sign_in_with_email_and_password(credential, password)
                        uid = firebase_user['localId']
                        # Se existe no Firebase, criar/sincronizar no Django
                        try:
                            user = User.objects.get(email=credential)
                            user.set_password(password)
                            user.save()
                        except User.DoesNotExist:
                            # Criar novo usuário Django a partir do Firebase
                            user = User.objects.create_user(
                                username=credential.split('@')[0],
                                email=credential,
                                password=password
                            )
                            logger.info(f"Criou usuário Django sincronizado com Firebase: {credential}")
                    except Exception as fb_error:
                        logger.warning(f"Firebase login fail for {credential}: {fb_error}")
                        messages.error(request, 'Usuário não encontrado. Verifique o e-mail/CPF ou registre-se.')

            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
                return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') or ''
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            cpf_cnpj = form.cleaned_data.get('cpf_cnpj')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            person_type = form.cleaned_data.get('person_type')
            state_registration = form.cleaned_data.get('state_registration')

            if not username and email:
                username = email.split('@')[0]

            try:
                # Criar usuário no Django primeiro
                user_django = form.save(commit=False)
                user_django.username = username.lower()
                user_django.first_name = first_name
                user_django.last_name = last_name
                user_django.save()

                # Cria perfil de usuário com dados adicionais
                UserProfile.objects.get_or_create(
                    user=user_django,
                    defaults={
                        'person_type': person_type,
                        'cpf_cnpj': cpf_cnpj,
                        'phone': phone,
                        'state_registration': state_registration or ''
                    }
                )

                # Cria/atualiza perfil de freelancer com PF/PJ
                from marketplace.models import FreelancerProfile
                profile, _ = FreelancerProfile.objects.get_or_create(user=user_django)
                profile.person_type = person_type
                profile.phone = phone
                if person_type == 'PF':
                    profile.cnpj = ''
                    profile.state_registration = ''
                else:
                    profile.business_name = f"{first_name} {last_name}".strip()
                    profile.cnpj = cpf_cnpj
                    profile.state_registration = state_registration or ''
                profile.save()

                # Tentar criar no Firebase
                firebase_uid = None
                try:
                    user_firebase = auth_firebase.create_user_with_email_and_password(email, password)
                    firebase_uid = user_firebase['localId']

                    if firebase_admin_initialized:
                        db = firestore.client()
                        cpf_digits = ''.join(ch for ch in cpf_cnpj if ch.isdigit())
                        user_data = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'cpf_cnpj': cpf_digits or cpf_cnpj.strip(),
                            'person_type': person_type
                        }
                        db.collection('users').document(firebase_uid).set(user_data)

                    auth_firebase.send_email_verification(user_firebase['idToken'])
                    messages.success(request, f'<i class="fas fa-check-circle"></i> Cadastro realizado com sucesso! Verifique seu e-mail.')
                except Exception as firebase_error:
                    logger.warning(f"Firebase error but user created in Django: {firebase_error}")
                    messages.success(request, f'<i class="fas fa-check-circle"></i> Cadastro realizado com sucesso! Faça login para continuar.')

                return redirect('login')

            except HTTPError as e:
                error_json = e.args[1]
                error_data = json.loads(error_json)
                error_message = error_data['error']['message']
                
                if 'EMAIL_EXISTS' in error_message:
                    messages.error(request, 'Este e-mail já está em uso.')
                elif 'WEAK_PASSWORD' in error_message:
                    messages.error(request, 'Senha muito fraca.')
                else:
                    messages.error(request, f'Erro no registro: {error_message}')
            
            except Exception as e:
                logger.error(f"Registration error: {e}")
                messages.error(request, f'Erro inesperado: {e}')
    else:
        form = UserRegisterForm()
    
    return render(request, 'core/register.html', {'form': form})


@login_required
def profile_view(request):
    from marketplace.models import FreelancerProfile
    profile, created = FreelancerProfile.objects.get_or_create(user=request.user)
    from marketplace.forms import FreelancerProfileForm
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user_form.save()
                profile_form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('profile')
            except Exception as e:
                messages.error(request, f'Erro ao salvar: {e}')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = FreelancerProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'core/profile.html', context)


def landing_view(request):
    """Landing page de onboarding - aparece antes do login"""
    return render(request, 'core/landing.html')


@login_required
def home_view(request):
    from django.shortcuts import redirect
    from marketplace.models import FreelancerProfile
    
    profile = FreelancerProfile.objects.filter(user=request.user).first()
    if profile:
        if profile.person_type == 'PF':
            return redirect('marketplace:pf_dashboard')
        elif profile.person_type == 'PJ':
            return redirect('marketplace:pj_dashboard')
    
    return render(request, 'core/home.html', {'freelancer_profile': profile})


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


def setup_admin_view(request):
    # Apenas permitir em DEBUG para não expor em produção.
    from django.conf import settings
    if not settings.DEBUG:
        messages.error(request, 'Acesso bloqueado fora do modo de desenvolvimento.')
        return redirect('login')

    username = request.GET.get('username', 'admin')
    email = request.GET.get('email', 'admin@nexuslife.com')
    password = request.GET.get('password', 'Nexus@123')

    if User.objects.filter(username=username).exists():
        messages.info(request, f'O usuário {username} já existe. Faça login em /admin')
        return redirect('login')

    User.objects.create_superuser(username=username, email=email, password=password)
    messages.success(request, f'Superuser criado: {username} / {password}. Acesse /admin')
    return redirect('login')


def chatbot_view(request):
    """View para exibir a interface do chatbot"""
    return render(request, 'core/chatbot.html')


@login_required
def notifications_view(request):
    """View para exibir todas as notificações do usuário"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'core/notifications.html', context)


@login_required
def mark_notification_as_read(request, notification_id):
    """Marcar uma notificação como lida"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.mark_as_read()
        messages.success(request, 'Notificação marcada como lida.')
    except Notification.DoesNotExist:
        messages.error(request, 'Notificação não encontrada.')
    
    return redirect('notifications')


@login_required
def mark_all_notifications_as_read(request):
    """Marcar todas as notificações como lidas"""
    Notification.objects.filter(user=request.user, is_read=False).update(
        is_read=True, 
        read_at=timezone.now()
    )
    messages.success(request, 'Todas as notificações foram marcadas como lidas.')
    return redirect('notifications')


@login_required
def get_unread_count(request):
    """API endpoint para obter contagem de notificações não lidas (JSON)"""
    from django.http import JsonResponse
    from django.utils import timezone
    
    unread_count = Notification.objects.filter(
        user=request.user, 
        is_read=False
    ).count()
    
    recent_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    notifications_list = [
        {
            'id': notif.id,
            'message': notif.message,
            'notification_type': notif.notification_type,
            'is_read': notif.is_read,
            'created_at': notif.created_at.isoformat(),
        }
        for notif in recent_notifications
    ]
    
    return JsonResponse({
        'unread_count': unread_count,
        'recent_notifications': notifications_list,
    })

