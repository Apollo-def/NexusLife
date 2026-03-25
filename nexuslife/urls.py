from django.contrib import admin
from django.urls import path, include
from core import views  # Isso está correto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    
    # Rotas do Gmail
    path('api/gmail/', include('core.gmail.urls')),
]