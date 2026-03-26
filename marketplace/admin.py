from django.contrib import admin
from .models import Category, Service, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'freelancer', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'freelancer__username']
    raw_id_fields = ['freelancer']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'client', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['service__title', 'client__username']
    raw_id_fields = ['service', 'client']
