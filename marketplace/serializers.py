from rest_framework import serializers
from .models import Category, Service, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    freelancer = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'price', 'category', 'freelancer', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['freelancer']

class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'category']

class OrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    client = serializers.StringRelatedField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'service', 'client', 'status', 'status_display', 'created_at', 'updated_at', 'notes']
        read_only_fields = ['client']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['notes']