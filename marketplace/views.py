from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import Category, Service, Order, Review
from .forms import ServiceForm, OrderForm
from core.models import Notification

from django.http import JsonResponse

def search_suggestions(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})
    services = Service.objects.filter(
        is_active=True
    ).filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(category__name__icontains=q)
    ).select_related('category')[:8]
    results = [
        {
            'id': s.pk,
            'title': s.title,
            'category': s.category.name,
            'price': str(s.price),
        }
        for s in services
    ]
    return JsonResponse({'results': results})

def service_list(request):
    services = Service.objects.filter(is_active=True).select_related('category', 'freelancer')
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    query = request.GET.get('q', '').strip()
    if category_filter:
        services = services.filter(category_id=category_filter)
    if query:
        services = services.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(freelancer__username__icontains=query) |
            Q(freelancer__first_name__icontains=query)
        )
    return render(request, 'marketplace/service_list.html', {
        'services': services,
        'categories': categories,
        'selected_category': category_filter,
        'query': query,
    })

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    return render(request, 'marketplace/service_detail.html', {'service': service})

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.freelancer = request.user
            service.save()
            messages.success(request, 'Serviço criado com sucesso!')
            return redirect('marketplace:service_detail', pk=service.pk)
    else:
        form = ServiceForm()
    return render(request, 'marketplace/service_form.html', {'form': form, 'title': 'Criar Serviço'})

@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk, freelancer=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('marketplace:service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'marketplace/service_form.html', {'form': form, 'title': 'Editar Serviço'})

@login_required
def order_create(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk, is_active=True)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.service = service
            order.client = request.user
            order.save()
            messages.success(request, 'Pedido realizado com sucesso!')
            return redirect('marketplace:order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'marketplace/order_form.html', {'form': form, 'service': service})

@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.all().select_related('service', 'client', 'service__freelancer')
    else:
        orders = Order.objects.filter(client=request.user).select_related('service', 'service__freelancer')
    return render(request, 'marketplace/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not (request.user == order.client or request.user == order.service.freelancer or request.user.is_staff):
        return redirect('marketplace:service_list')
    return render(request, 'marketplace/order_detail.html', {'order': order})

@login_required
def order_update_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk, service__freelancer=request.user)
    if status in dict(Order.STATUS_CHOICES):
        order.status = status
        order.save()
        messages.success(request, f'Status do pedido atualizado para {order.get_status_display()}!')
    return redirect('marketplace:order_detail', pk=order.pk)


from django.db.models import Q

@login_required
def pf_dashboard(request):
    """Dashboard Pessoa Física"""
    profile = getattr(request.user, 'freelancer_profile', None)
    if not profile or profile.person_type != 'PF':
        messages.warning(request, 'Dashboard PF - redirecionando...')
        return redirect('home')

    services = Service.objects.filter(freelancer=request.user, is_active=True)
    orders = Order.objects.filter(service__freelancer=request.user).select_related('service', 'client').order_by('-created_at')[:5]
    
    # Projetos publicados por empresas (PJ) disponíveis para candidatura
    from core.models import UserProfile
    pj_users = UserProfile.objects.filter(person_type='PJ').values_list('user_id', flat=True)
    suggested_jobs = Service.objects.filter(
        is_active=True
    ).exclude(
        freelancer=request.user
    ).select_related('category', 'freelancer').order_by('-created_at')[:12]
    
    # Notificações
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Estatísticas
    total_orders = Order.objects.filter(service__freelancer=request.user).count()
    completed_orders = Order.objects.filter(service__freelancer=request.user, status='completed').count()
    pending_orders = Order.objects.filter(service__freelancer=request.user, status='pending').count()
    total_reviews = Review.objects.filter(service__freelancer=request.user).count()

    context = {
        'profile': profile,
        'services': services,
        'orders': orders,
        'suggested_jobs': suggested_jobs,
        'unread_notifications': unread_notifications,
        'recent_notifications': recent_notifications,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'total_reviews': total_reviews,
    }
    return render(request, 'marketplace/pf_dashboard.html', context)


@login_required
def pj_dashboard(request):
    """Dashboard Pessoa Jurídica"""
    profile = getattr(request.user, 'freelancer_profile', None)
    if not profile or profile.person_type != 'PJ':
        messages.warning(request, 'Dashboard PJ - redirecionando...')
        return redirect('home')

    services = Service.objects.filter(freelancer=request.user, is_active=True)
    orders = Order.objects.filter(service__freelancer=request.user).select_related('service', 'client').order_by('-created_at')[:5]
    
    # Notificações
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Estatísticas
    total_orders = Order.objects.filter(service__freelancer=request.user).count()
    completed_orders = Order.objects.filter(service__freelancer=request.user, status='completed').count()
    pending_orders = Order.objects.filter(service__freelancer=request.user, status='pending').count()
    total_reviews = Review.objects.filter(service__freelancer=request.user).count()

    context = {
        'profile': profile,
        'services': services,
        'orders': orders,
        'unread_notifications': unread_notifications,
        'recent_notifications': recent_notifications,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'total_reviews': total_reviews,
    }
    return render(request, 'marketplace/pj_dashboard.html', context)
