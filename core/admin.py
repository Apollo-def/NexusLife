from django.contrib import admin
from .models import UserProfile, Notification, ChatbotConversation, ChatbotMessage

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


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at', 'read_at')
    fieldsets = (
        ('Notificação', {
            'fields': ('user', 'notification_type', 'title', 'message', 'is_read')
        }),
        ('Dados', {
            'fields': ('icon', 'link', 'created_at', 'read_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatbotConversation)
class ChatbotConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'session_id', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'title', 'session_id')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Conversa', {
            'fields': ('session_id', 'user', 'title', 'is_active')
        }),
        ('Dados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ChatbotMessageInline(admin.TabularInline):
    model = ChatbotMessage
    extra = 0
    readonly_fields = ('created_at', 'sender', 'message', 'tokens_used')
    can_delete = False
    fields = ('sender', 'message', 'tokens_used', 'created_at')


@admin.register(ChatbotMessage)
class ChatbotMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'created_at', 'tokens_used')
    list_filter = ('sender', 'created_at')
    search_fields = ('conversation__title', 'message')
    readonly_fields = ('created_at', 'message')
    fieldsets = (
        ('Mensagem', {
            'fields': ('conversation', 'sender', 'message')
        }),
        ('Dados', {
            'fields': ('tokens_used', 'created_at'),
            'classes': ('collapse',)
        }),
    )

