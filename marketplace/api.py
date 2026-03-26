from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Avg, Count
from .models import Category, Service, Order, Review, Favorite, FreelancerProfile
from .serializers import (
    CategorySerializer, ServiceSerializer, ServiceCreateSerializer,
    OrderSerializer, OrderCreateSerializer, ReviewSerializer, ReviewCreateSerializer,
    FavoriteSerializer, FreelancerProfileSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category__name']
    ordering_fields = ['price', 'created_at', '-average_rating']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related(
            'category', 'freelancer', 'freelancer__freelancer_profile'
        ).prefetch_related('reviews')

        # Filtros
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        freelancer = self.request.query_params.get('freelancer')
        if freelancer:
            queryset = queryset.filter(freelancer_id=freelancer)

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ServiceCreateSerializer
        return ServiceSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(freelancer=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_services(self, request):
        """Meus serviços como freelancer"""
        services = Service.objects.filter(
            freelancer=request.user
        ).select_related('category', 'freelancer__freelancer_profile').prefetch_related('reviews')
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Todas as avaliações de um serviço"""
        service = self.get_object()
        reviews = service.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        """Adicionar/remover dos favoritos"""
        service = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, service=service)

        if not created:
            favorite.delete()
            return Response({'favorited': False, 'message': 'Removido dos favoritos'})

        return Response({'favorited': True, 'message': 'Adicionado aos favoritos'})

class FreelancerProfileViewSet(viewsets.ModelViewSet):
    queryset = FreelancerProfile.objects.all()
    serializer_class = FreelancerProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'user_id'

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Meu perfil de freelancer"""
        profile, created = FreelancerProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Atualizar meu perfil"""
        profile, created = FreelancerProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.user
        # Both as client and as freelancer
        return Order.objects.filter(
            Q(client=user) | Q(service__freelancer=user)
        ).select_related('service', 'service__category', 'service__freelancer').prefetch_related('review')

    @property
    def user(self):
        return self.request.user

    def perform_create(self, serializer):
        service_id = self.request.data.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        serializer.save(
            client=self.request.user,
            service=service,
            amount=service.price
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        """Atualizar status do pedido"""
        order = self.get_object()

        # Only freelancer can update status
        if order.service.freelancer != request.user:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            if new_status == 'completed':
                order.completed_at = timezone.now()
            order.save()
            return Response(self.get_serializer(order).data)

        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def review(self, request, pk=None):
        """Deixar avaliação para um pedido"""
        order = self.get_object()

        # Only client can review
        if order.client != request.user:
            return Response(
                {'error': 'Only client can review'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        if order.status != 'completed':
            return Response(
                {'error': 'Can only review completed orders'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                order=order,
                service=order.service,
                reviewer=request.user
            )
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_orders(self, request):
        """Meus pedidos como cliente"""
        orders = Order.objects.filter(client=request.user).select_related(
            'service', 'service__category', 'service__freelancer'
        ).prefetch_related('review')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def incoming_orders(self, request):
        """Pedidos recebidos como freelancer"""
        orders = Order.objects.filter(
            service__freelancer=request.user
        ).select_related('service', 'client').prefetch_related('review')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Listar meus favoritos"""
        favorites = Favorite.objects.filter(user=request.user).select_related('service')
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Adicionar favorito"""
        service_id = request.data.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, service=service)
        serializer = FavoriteSerializer(favorite)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def remove(self, request):
        """Remover favorito"""
        service_id = request.data.get('service_id')
        Favorite.objects.filter(user=request.user, service_id=service_id).delete()
        return Response({'message': 'Favorito removido'})

class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=False, methods=['get'])
    def by_freelancer(self, request):
        """Avaliações de um freelancer"""
        freelancer_id = request.query_params.get('freelancer_id')
        if not freelancer_id:
            return Response(
                {'error': 'freelancer_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        reviews = Review.objects.filter(service__freelancer_id=freelancer_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)