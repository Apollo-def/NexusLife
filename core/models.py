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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuário'

    def __str__(self):
        return f"{self.user.username} - {self.get_person_type_display()}"
