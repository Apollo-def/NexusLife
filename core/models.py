from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    PERSON_TYPE_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    person_type = models.CharField(max_length=2, choices=PERSON_TYPE_CHOICES, default='PF')
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    phone = models.CharField(max_length=20)
    state_registration = models.CharField(max_length=20, blank=True, null=True)
    average_rating = models.FloatField(default=0.0)
    completion_rate = models.FloatField(default=0.0)
    total_earnings = models.FloatField(default=0.0)
    response_time = models.IntegerField(default=24, help_text="Tempo em horas")
    total_reviews = models.IntegerField(default=0)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuário'

    def __str__(self):
        return f"{self.user.username} - {self.get_person_type_display()}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order', 'Novo Pedido'),
        ('order_updated', 'Pedido Atualizado'),
        ('review', 'Nova Avaliação'),
        ('message', 'Nova Mensagem'),
        ('payment', 'Pagamento'),
        ('account', 'Conta'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    icon = models.CharField(max_length=50, default='fas fa-bell')
    link = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def mark_as_read(self):
        """Marca notificação como lida"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class ChatbotConversation(models.Model):
    """Armazena histórico de conversas com o chatbot"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatbot_conversations', null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255, blank=True, default='Conversa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Conversa Chatbot'
        verbose_name_plural = 'Conversas Chatbot'
        ordering = ['-updated_at']

    def __str__(self):
        user_str = self.user.username if self.user else "Anônimo"
        return f"{self.title} ({user_str})"


class ChatbotMessage(models.Model):
    """Armazena mensagens individuais da conversa"""
    SENDER_CHOICES = [
        ('user', 'Usuário'),
        ('bot', 'Bot'),
    ]
    
    conversation = models.ForeignKey(ChatbotConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    tokens_used = models.IntegerField(default=0, help_text="Tokens de OpenAI usados")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem Chatbot'
        verbose_name_plural = 'Mensagens Chatbot'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}..."
