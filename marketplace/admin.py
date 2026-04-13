from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Service, Order, Review, Favorite, FreelancerProfile


# Customizar Admin Site
admin.site.site_header = "🚀 NexusLife - Painel Administrativo"
admin.site.site_title = "Admin NexusLife"
admin.site.index_title = "Bem-vindo ao Painel de Administração"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_with_emoji', 'total_services', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'total_services_display']
    
    fieldsets = (
        ('📂 Categoria', {
            'fields': ('name',)
        }),
        ('📊 Estatísticas', {
            'fields': ('total_services_display',),
            'classes': ('collapse',)
        }),
        ('🕐 Data', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def name_with_emoji(self, obj):
        emojis = {
            'design': '🎨',
            'development': '💻',
            'writing': '✍️',
            'marketing': '📢',
            'video': '🎥',
            'music': '🎵',
        }
        emoji = emojis.get(obj.name.lower(), '📦')
        return format_html('{} {}', emoji, obj.name)
    name_with_emoji.short_description = '📂 Categoria'
    
    def total_services(self, obj):
        count = obj.service_set.count()
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            count
        )
    total_services.short_description = '📦 Serviços'
    
    def total_services_display(self, obj):
        return obj.service_set.count()
    total_services_display.short_description = 'Total de Serviços'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'title_link',
        'freelancer_link',
        'category_badge',
        'price_display',
        'status_badge',
        'rating_display',
        'total_orders',
        'created_at'
    ]
    list_filter = [
        'category',
        'is_active',
        'created_at',
    ]
    search_fields = ['title', 'description', 'freelancer__user__username', 'freelancer__user__email']
    raw_id_fields = ['freelancer']
    readonly_fields = ['created_at', 'updated_at', 'service_info_display']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('📝 Informações do Serviço', {
            'fields': ('title', 'description', 'category', 'freelancer')
        }),
        ('💰 Preço e Disponibilidade', {
            'fields': ('price', 'is_active'),
        }),
        ('⭐ Avaliações', {
            'fields': ('average_rating', 'total_orders'),
            'classes': ('collapse',)
        }),
        ('ℹ️ Resumo', {
            'fields': ('service_info_display',),
            'classes': ('collapse',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
    
    def title_link(self, obj):
        return format_html(
            '<a href="{}" style="color: #0066cc; font-weight: bold;">{}</a>',
            reverse('admin:marketplace_service_change', args=[obj.id]),
            obj.title[:40] + '...' if len(obj.title) > 40 else obj.title
        )
    title_link.short_description = '📝 Serviço'
    
    def freelancer_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.freelancer.user.id])
        return format_html(
            '<a href="{}" style="color: #0066cc;">{}</a>',
            url,
            obj.freelancer.user.get_full_name() or obj.freelancer.user.username
        )
    freelancer_link.short_description = '👤 Freelancer'
    
    def category_badge(self, obj):
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px;">📂 {}</span>',
            obj.category.name
        )
    category_badge.short_description = '📂 Categoria'
    
    def price_display(self, obj):
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">R$ {:.2f}</span>',
            obj.price
        )
    price_display.short_description = '💰 Preço'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">✓ Ativo</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">✗ Inativo</span>'
            )
    status_badge.short_description = '🔴 Status'
    
    def rating_display(self, obj):
        stars = '⭐' * int(obj.average_rating) if obj.average_rating else '☆ Sem avaliações'
        return format_html(
            '{} <strong>{:.1f}</strong>/5.0',
            stars,
            obj.average_rating if obj.average_rating else 0
        )
    rating_display.short_description = '⭐ Avaliação'
    
    def service_info_display(self, obj):
        return format_html(
            '<div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;"><strong>Descrição:</strong> {}<br><strong>Pedidos:</strong> {}</div>',
            obj.description[:100] + '...' if len(obj.description) > 100 else obj.description,
            obj.total_orders
        )
    service_info_display.short_description = 'ℹ️ Informações'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id_badge',
        'service_link',
        'client_link',
        'status_badge',
        'amount_display',
        'created_at'
    ]
    list_filter = [
        'status',
        'created_at',
    ]
    search_fields = [
        'service__title',
        'client__user__username',
        'client__user__email',
        'id'
    ]
    raw_id_fields = ['service', 'client']
    readonly_fields = ['created_at', 'updated_at', 'completed_at', 'order_info_display']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('📦 Informações do Pedido', {
            'fields': ('id', 'service', 'client')
        }),
        ('💰 Valores', {
            'fields': ('amount',),
        }),
        ('🔧 Status', {
            'fields': ('status',),
        }),
        ('ℹ️ Resumo', {
            'fields': ('order_info_display',),
            'classes': ('collapse',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
    
    def order_id_badge(self, obj):
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">#{}</span>',
            obj.id
        )
    order_id_badge.short_description = '🆔 Pedido'
    
    def service_link(self, obj):
        url = reverse('admin:marketplace_service_change', args=[obj.service.id])
        return format_html(
            '<a href="{}" style="color: #0066cc;">{}</a>',
            url,
            obj.service.title[:30] + '...' if len(obj.service.title) > 30 else obj.service.title
        )
    service_link.short_description = '📝 Serviço'
    
    def client_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.client.user.id])
        return format_html(
            '<a href="{}" style="color: #0066cc;">{}</a>',
            url,
            obj.client.user.get_full_name() or obj.client.user.username
        )
    client_link.short_description = '👤 Cliente'
    
    def status_badge(self, obj):
        status_colors = {
            'pending': '#ffc107',
            'in_progress': '#007bff',
            'completed': '#28a745',
            'cancelled': '#dc3545'
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = '🔧 Status'
    
    def amount_display(self, obj):
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">R$ {:.2f}</span>',
            obj.amount
        )
    amount_display.short_description = '💰 Valor'
    
    def order_info_display(self, obj):
        return format_html(
            '<div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;"><strong>ID:</strong> {}<br><strong>Serviço:</strong> {}<br><strong>Cliente:</strong> {}</div>',
            obj.id,
            obj.service.title,
            obj.client.user.get_full_name() or obj.client.user.username
        )
    order_info_display.short_description = 'ℹ️ Informações'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'review_id_badge',
        'service_link',
        'reviewer_link',
        'rating_stars',
        'comment_preview',
        'created_at'
    ]
    list_filter = [
        'rating',
        'created_at',
    ]
    search_fields = [
        'service__title',
        'reviewer__user__username',
        'reviewer__user__email',
        'comment'
    ]
    raw_id_fields = ['order', 'service', 'reviewer']
    readonly_fields = ['created_at', 'updated_at', 'review_info_display']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('⭐ Avaliação', {
            'fields': ('service', 'reviewer', 'rating', 'comment')
        }),
        ('📦 Pedido Relacionado', {
            'fields': ('order',),
            'classes': ('collapse',)
        }),
        ('ℹ️ Resumo', {
            'fields': ('review_info_display',),
            'classes': ('collapse',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
    
    def review_id_badge(self, obj):
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">#{}</span>',
            obj.id
        )
    review_id_badge.short_description = '🆔 Review'
    
    def service_link(self, obj):
        url = reverse('admin:marketplace_service_change', args=[obj.service.id])
        return format_html(
            '<a href="{}" style="color: #0066cc;">{}</a>',
            url,
            obj.service.title[:30] + '...' if len(obj.service.title) > 30 else obj.service.title
        )
    service_link.short_description = '📝 Serviço'
    
    def reviewer_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.reviewer.user.id])
        return format_html(
            '<a href="{}" style="color: #0066cc;">{}</a>',
            url,
            obj.reviewer.user.get_full_name() or obj.reviewer.user.username
        )
    reviewer_link.short_description = '👤 Avaliador'
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html('{} <strong>{}/5.0</strong>', stars, obj.rating)
    rating_stars.short_description = '⭐ Nota'
    
    def comment_preview(self, obj):
        preview = obj.comment[:40] + '...' if len(obj.comment) > 40 else obj.comment
        return preview
    comment_preview.short_description = '💬 Comentário'
    
    def review_info_display(self, obj):
        return format_html(
            '<div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;"><strong>Avaliador:</strong> {}<br><strong>Serviço:</strong> {}<br><strong>Nota:</strong> ⭐ {}/5</div>',
            obj.reviewer.user.get_full_name() or obj.reviewer.user.username,
            obj.service.title,
            obj.rating
        )
    review_info_display.short_description = 'ℹ️ Informações'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = [
        'favorite_id_badge',
        'user_link',
        'service_link',
        'created_at'
    ]
    list_filter = ['created_at']
    search_fields = [
        'user__user__username',
        'user__user__email',
        'service__title'
    ]
    raw_id_fields = ['user', 'service']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('❤️ Favorito', {
            'fields': ('user', 'service')
        }),
        ('🕐 Data', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
    
    def favorite_id_badge(self, obj):
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">❤️ #{}</span>',
            obj.id
        )
    favorite_id_badge.short_description = '❤️ ID'
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.user.id])
        return format_html(
            '<a href="{}" style="color: #0066cc;">{}</a>',
            url,
            obj.user.user.get_full_name() or obj.user.user.username
        )
    user_link.short_description = '👤 Usuário'
    
    def service_link(self, obj):
        url = reverse('admin:marketplace_service_change', args=[obj.service.id])
        return format_html(
            '<a href="{}" style="color: #0066cc;">{}</a>',
            url,
            obj.service.title
        )
    service_link.short_description = '📝 Serviço'


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_link',
        'rating_display',
        'total_reviews_badge',
        'completion_rate_bar',
        'verified_badge',
        'earnings_display'
    ]
    list_filter = [
        'verified',
        'created_at',
    ]
    search_fields = [
        'user__user__username',
        'user__user__email',
        'bio'
    ]
    raw_id_fields = ['user']
    readonly_fields = [
        'created_at',
        'updated_at',
        'total_earnings',
        'profile_info_display'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('👤 Perfil', {
            'fields': ('user', 'bio', 'verified')
        }),
        ('⭐ Estatísticas', {
            'fields': ('average_rating', 'total_reviews', 'completion_rate', 'total_earnings')
        }),
        ('ℹ️ Resumo', {
            'fields': ('profile_info_display',),
            'classes': ('collapse',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.user.id])
        return format_html(
            '<a href="{}" style="color: #0066cc; font-weight: bold;">{}</a>',
            url,
            obj.user.user.get_full_name() or obj.user.user.username
        )
    user_link.short_description = '👤 Freelancer'
    
    def rating_display(self, obj):
        rating = obj.average_rating if obj.average_rating else 0
        stars = '⭐' * int(rating)
        return format_html(
            '{} <strong>{:.1f}</strong>/5.0',
            stars,
            rating
        )
    rating_display.short_description = '⭐ Avaliação'
    
    def total_reviews_badge(self, obj):
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">💬 {}</span>',
            obj.total_reviews
        )
    total_reviews_badge.short_description = '💬 Avaliações'
    
    def completion_rate_bar(self, obj):
        rate = obj.completion_rate if obj.completion_rate else 0
        color = '#28a745' if rate >= 90 else '#ffc107' if rate >= 70 else '#dc3545'
        return format_html(
            '<div style="background-color: #e9ecef; border-radius: 10px; overflow: hidden; width: 100px; height: 20px;"><div style="background-color: {}; width: {}%; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{:.0f}%</div></div>',
            color,
            rate,
            rate
        )
    completion_rate_bar.short_description = '📊 Taxa de Conclusão'
    
    def verified_badge(self, obj):
        if obj.verified:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">✓ Verificado</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">⏳ Pendente</span>'
            )
    verified_badge.short_description = '✅ Status'
    
    def earnings_display(self, obj):
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">R$ {:.2f}</span>',
            obj.total_earnings if obj.total_earnings else 0
        )
    earnings_display.short_description = '💰 Ganhos'
    
    def profile_info_display(self, obj):
        return format_html(
            '<div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;"><strong>Bio:</strong> {}<br><strong>Avaliação:</strong> ⭐ {:.1f}/5<br><strong>Taxa de Conclusão:</strong> {:.0f}%<br><strong>Ganhos Totais:</strong> R$ {:.2f}</div>',
            obj.bio[:100] + '...' if len(obj.bio or '') > 100 else obj.bio,
            obj.average_rating if obj.average_rating else 0,
            obj.completion_rate if obj.completion_rate else 0,
            obj.total_earnings if obj.total_earnings else 0
        )
    profile_info_display.short_description = 'ℹ️ Informações'
