from django.contrib import admin
from .models import Category, Service, Order, Review, Favorite, FreelancerProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'freelancer', 'category', 'price', 'is_active', 'average_rating', 'total_orders', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'freelancer__username']
    raw_id_fields = ['freelancer']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'client', 'status', 'amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['service__title', 'client__username']
    raw_id_fields = ['service', 'client']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['service__title', 'reviewer__username']
    raw_id_fields = ['order', 'service', 'reviewer']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'service', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'service__title']
    raw_id_fields = ['user', 'service']
    readonly_fields = ['created_at']

@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'average_rating', 'total_reviews', 'completion_rate', 'verified', 'total_earnings']
    list_filter = ['verified', 'created_at']
    search_fields = ['user__username', 'bio']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at', 'total_earnings']
