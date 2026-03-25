from django.db import models
from django.conf import settings

class GmailToken(models.Model):
    """Armazena tokens OAuth do Gmail"""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gmail_token'
    )
    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField()
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gmail_tokens'
        verbose_name = 'Token Gmail'
        verbose_name_plural = 'Tokens Gmail'
    
    def __str__(self):
        return f"{self.email} - {self.user.username}"