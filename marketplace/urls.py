from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

router = DefaultRouter()
router.register(r'categories', api.CategoryViewSet)
router.register(r'services', api.ServiceViewSet)
router.register(r'orders', api.OrderViewSet)

app_name = 'marketplace'

urlpatterns = [
    # Web views
    path('', views.service_list, name='service_list'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('service/create/', views.service_create, name='service_create'),
    path('service/<int:pk>/update/', views.service_update, name='service_update'),
    path('service/<int:service_pk>/order/', views.order_create, name='order_create'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/<int:pk>/status/<str:status>/', views.order_update_status, name='order_update_status'),

    # API views
    path('api/', include(router.urls)),
]