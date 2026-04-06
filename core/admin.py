from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'person_type', 'cpf_cnpj', 'phone', 'created_at')
    list_filter = ('person_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'cpf_cnpj')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Pessoais', {
            'fields': ('person_type', 'cpf_cnpj', 'phone', 'state_registration')
        }),
        ('Data', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
