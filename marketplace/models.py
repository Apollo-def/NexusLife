from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome class name")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', verbose_name='Categoria')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services', verbose_name='Freelancer')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    
    # Meta informações
    delivery_days = models.PositiveIntegerField(default=7, help_text="Prazo de entrega em dias", verbose_name='Prazo de Entrega')
    revisions = models.PositiveIntegerField(default=2, help_text="Número de revisões incluídas", verbose_name='Revisões')
    
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['freelancer', 'is_active']),
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0

    @property
    def total_orders(self):
        return self.orders.filter(status='completed').count()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('disputed', 'Em Disputa'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_as_client')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client', 'status']),
            models.Index(fields=['service', 'status']),
        ]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.service.title}"

class Review(models.Model):
    """Avaliação de um serviço completado"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-created_at']
        unique_together = ['order', 'service']

    def __str__(self):
        return f"{self.reviewer.username} - {self.service.title} ({self.rating}★)"

class Favorite(models.Model):
    """Serviços favoritados pelo usuário"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        unique_together = ['user', 'service']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"

class FreelancerProfile(models.Model):
    """Perfil estendido do freelancer"""

    PERSON_TYPE_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='freelancer_profile')
    person_type = models.CharField(max_length=2, choices=PERSON_TYPE_CHOICES, default='PF')
    business_name = models.CharField(max_length=150, blank=True, help_text='Para Pessoa Jurídica')
    cnpj = models.CharField(max_length=18, blank=True, help_text='Para Pessoa Jurídica')
    state_registration = models.CharField(max_length=20, blank=True, help_text='Inscrição Estadual para PJ')
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    verified = models.BooleanField(default=False)
    response_time = models.PositiveIntegerField(default=24, help_text="Tempo de resposta em horas")
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Freelancer'
        verbose_name_plural = 'Perfis de Freelancer'

    def __str__(self):
        return f"Perfil de {self.user.username}"

    @property
    def average_rating(self):
        reviews = Review.objects.filter(service__freelancer=self.user)
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0

    @property
    def total_reviews(self):
        return Review.objects.filter(service__freelancer=self.user).count()

    @property
    def completion_rate(self):
        total = self.user.services.aggregate(
            total=models.Count('orders')
        )['total'] or 1
        completed = self.user.services.aggregate(
            completed=models.Count('orders', filter=models.Q(orders__status='completed'))
        )['completed'] or 0
        return (completed / total * 100) if total > 0 else 0
