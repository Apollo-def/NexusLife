from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Service, Order
from .forms import ServiceForm, OrderForm

def service_list(request):
    services = Service.objects.filter(is_active=True).select_related('category', 'freelancer')
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    if category_filter:
        services = services.filter(category_id=category_filter)
    return render(request, 'marketplace/service_list.html', {
        'services': services,
        'categories': categories,
        'selected_category': category_filter,
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
