from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import UserProfile, Notification, ChatbotConversation, ChatbotMessage


# Customizar o Admin Site padrão (sem substituir a instância global)
admin.site.site_header = "🚀 NexusLife - Painel Administrativo"
admin.site.site_title = "Admin NexusLife"
admin.site.index_title = "Bem-vindo ao Painel de Administração"

# Customizar o método index do admin
original_index = admin.site.index

def custom_index(request, extra_context=None):
    """Adiciona estatísticas ao index do admin"""
    from marketplace.models import Service, Order, Review
    
    extra_context = extra_context or {}
    extra_context.update({
        'total_users': User.objects.count(),
        'total_services': Service.objects.filter(is_active=True).count(),
        'total_orders': Order.objects.count(),
        'total_reviews': Review.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'completed_orders': Order.objects.filter(status='completed').count(),
        'total_notifications': Notification.objects.count(),
        'unread_notifications': Notification.objects.filter(is_read=False).count(),
        'total_conversations': ChatbotConversation.objects.count(),
        'active_conversations': ChatbotConversation.objects.filter(is_active=True).count(),
        'total_chatbot_messages': ChatbotMessage.objects.count(),
    })
    return original_index(request, extra_context)

admin.site.index = custom_index


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('person_type', 'cpf_cnpj', 'phone', 'state_registration')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'person_type', 'cpf_cnpj', 'phone', 'created_at')
    list_filter = ('person_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'cpf_cnpj', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'notification_badge',
        'title_truncated',
        'read_status',
        'created_at'
    )
    list_filter = (
        'notification_type',
        'is_read',
        'created_at',
    )
    search_fields = ('user__username', 'user__email', 'title', 'message')
    readonly_fields = ('created_at', 'read_at', 'message_display')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('📨 Notificação', {
            'fields': ('user', 'notification_type', 'title', 'message_display')
        }),
        ('📌 Configurações', {
            'fields': ('is_read', 'icon', 'link'),
        }),
        ('🕐 Timestamp', {
            'fields': ('created_at', 'read_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
    
    def notification_badge(self, obj):
        icons = {
            'order': '📦',
            'review': '⭐',
            'message': '💬',
            'system': '⚙️'
        }
        icon = icons.get(obj.notification_type, '🔔')
        return format_html('{} {}', icon, obj.get_notification_type_display())
    notification_badge.short_description = '📨 Tipo'
    
    def title_truncated(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_truncated.short_description = '📝 Título'
    
    def read_status(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px;font-weight: bold;">✓ Lida</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ffc107; color: #333; padding: 3px 8px; border-radius: 3px; font-weight: bold;">⚡ Não Lida</span>'
            )
    read_status.short_description = '✉️ Status'
    
    def message_display(self, obj):
        return format_html(
            '<div style="background-color: #f9f9f9; padding: 10px; border-left: 4px solid #007bff; border-radius: 4px; word-wrap: break-word;">{}</div>',
            obj.message
        )
    message_display.short_description = '📄 Mensagem'


class ChatbotMessageInline(admin.TabularInline):
    model = ChatbotMessage
    extra = 0
    readonly_fields = ('created_at', 'message_preview')
    fields = ('sender', 'message_preview', 'created_at')
    can_delete = False
    
    def message_preview(self, obj):
        preview = obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
        return preview
    message_preview.short_description = 'Prévia da Mensagem'


@admin.register(ChatbotConversation)
class ChatbotConversationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'conversation_status',
        'message_count',
        'created_at'
    )
    list_filter = (
        'is_active',
        'created_at',
    )
    search_fields = ('user__username', 'user__email', 'title', 'session_id')
    date_hierarchy = 'created_at'
    inlines = [ChatbotMessageInline]
    ordering = ('-created_at',)
    list_per_page = 25
    
    def conversation_status(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">🟢 Ativa</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">⚫ Fechada</span>'
            )
    conversation_status.short_description = '🟢 Status'
    
    def message_count(self, obj):
        count = obj.messages.count()
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">💬 {}</span>',
            count
        )
    message_count.short_description = '💬 Mensagens'


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


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'user_badge',
        'email_link',
        'user_type_badge',
        'is_active_badge',
        'date_joined_display',
        'last_login_display'
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = (
        'date_joined',
        'last_login',
        'user_info_display',
        'permissions_display'
    )
    date_hierarchy = 'date_joined'
    
    fieldsets = (
        ('👤 Informações Básicas', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('🔐 Segurança', {
            'fields': ('password', 'is_active'),
        }),
        ('👨‍💼 Permissões', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('ℹ️ Informações Adicionais', {
            'fields': ('user_info_display', 'permissions_display'),
            'classes': ('collapse',)
        }),
        ('🕐 Histórico', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-date_joined',)
    list_per_page = 25
    filter_horizontal = ('groups', 'user_permissions')
    
    def user_badge(self, obj):
        full_name = obj.get_full_name() or obj.username
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">👤 {}</span>',
            full_name
        )
    user_badge.short_description = '👤 Usuário'
    
    def email_link(self, obj):
        return format_html(
            '<a href="mailto:{}" style="color: #0066cc; font-weight: 600;">{}</a>',
            obj.email,
            obj.email
        )
    email_link.short_description = '📧 Email'
    
    def user_type_badge(self, obj):
        if obj.is_superuser:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">👑 Superadmin</span>'
            )
        elif obj.is_staff:
            return format_html(
                '<span style="background-color: #ffc107; color: #333; padding: 3px 8px; border-radius: 3px; font-weight: bold;">👨‍💼 Staff</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">👤 Usuário</span>'
            )
    user_type_badge.short_description = '👨‍💼 Tipo'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">✓ Ativo</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">✗ Bloqueado</span>'
            )
    is_active_badge.short_description = '🔴 Status'
    
    def date_joined_display(self, obj):
        return format_html(
            '<strong>📅 {}</strong>',
            obj.date_joined.strftime('%d/%m/%Y às %H:%M')
        )
    date_joined_display.short_description = '📅 Cadastro'
    
    def last_login_display(self, obj):
        if obj.last_login:
            return format_html(
                '<strong>🕐 {}</strong>',
                obj.last_login.strftime('%d/%m/%Y às %H:%M')
            )
        else:
            return format_html('<em style="color: #999;">Nunca acessou</em>')
    last_login_display.short_description = '🕐 Último Acesso'
    
    def user_info_display(self, obj):
        return format_html(
            '<div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff;"><strong>👤 Nome:</strong> {} {}<br><strong>📧 Email:</strong> {}<br><strong>🆔 Username:</strong> {}<br><strong>📅 Cadastro:</strong> {}<br><strong>🕐 Último Acesso:</strong> {}</div>',
            obj.first_name,
            obj.last_name,
            obj.email,
            obj.username,
            obj.date_joined.strftime('%d/%m/%Y às %H:%M'),
            obj.last_login.strftime('%d/%m/%Y às %H:%M') if obj.last_login else 'Nunca'
        )
    user_info_display.short_description = 'ℹ️ Informações do Usuário'
    
    def permissions_display(self, obj):
        perms = []
        if obj.is_active:
            perms.append('Ativo')
        if obj.is_staff:
            perms.append('Staff')
        if obj.is_superuser:
            perms.append('Superadmin')
        if not perms:
            perms = ['Usuário Regular']
        
        return format_html(
            '<div style="background-color: #f0f7ff; padding: 10px; border-radius: 5px; border-left: 4px solid #007bff;"><strong>Permissões:</strong><br>{}</div>',
            '<br>'.join(['✓ ' + p for p in perms])
        )
    permissions_display.short_description = '🔐 Permissões'

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
