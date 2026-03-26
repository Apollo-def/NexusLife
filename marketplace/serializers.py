from rest_framework import serializers
from .models import Category, Service, Order, Review, Favorite, FreelancerProfile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'reviewer_username', 'rating', 'comment', 'created_at']

class FreelancerProfileSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = FreelancerProfile
        fields = [
            'id', 'username', 'bio', 'profile_image', 'hourly_rate',
            'location', 'phone', 'website', 'verified', 'response_time',
            'average_rating', 'total_reviews', 'completion_rate', 'total_earnings'
        ]
        read_only_fields = ['average_rating', 'total_reviews', 'completion_rate', 'total_earnings']

    def get_average_rating(self, obj):
        return round(obj.average_rating, 2)

    def get_total_reviews(self, obj):
        return obj.total_reviews

    def get_completion_rate(self, obj):
        return round(obj.completion_rate, 2)

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    freelancer_profile = FreelancerProfileSerializer(source='freelancer.freelancer_profile', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_orders = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'description', 'price', 'category', 'freelancer_profile',
            'is_active', 'delivery_days', 'revisions', 'average_rating', 'total_orders',
            'reviews', 'is_favorite', 'created_at', 'updated_at'
        ]
        read_only_fields = ['average_rating', 'total_orders']

    def get_average_rating(self, obj):
        return round(obj.average_rating, 2)

    def get_total_orders(self, obj):
        return obj.total_orders

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, service=obj).exists()
        return False

class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'category', 'delivery_days', 'revisions']

class OrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    client_username = serializers.CharField(source='client.username', read_only=True)
    freelancer_username = serializers.CharField(source='service.freelancer.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'service', 'client_username', 'freelancer_username', 'status',
            'status_display', 'created_at', 'updated_at', 'completed_at', 'notes', 'amount'
        ]
        read_only_fields = ['client_username', 'freelancer_username']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['notes']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class FavoriteSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source='service.title', read_only=True)
    service = ServiceSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'service', 'service_title', 'created_at']