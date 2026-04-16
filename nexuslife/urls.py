from django.contrib import admin
from django.urls import path, include
from core import views  # Isso está correto
from core.chatbot_enhanced import (
    chatbot_api, chatbot_conversations, chatbot_conversation_detail,
    delete_conversation, get_conversation
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_view, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/pf/', views.profile_view, name='pf_profile'),  # Reuse with context
    path('profile/pj/', views.profile_view, name='pj_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('setup-admin/', views.setup_admin_view, name='setup_admin'),
    
    # Chatbot (AI Enhanced)
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
    path('chatbot/', views.chatbot_view, name='chatbot_page'),
    path('api/chatbot/conversation/', get_conversation, name='get_conversation'),
    path('chatbot/conversations/', chatbot_conversations, name='chatbot_conversations'),
    path('chatbot/conversation/<str:session_id>/', chatbot_conversation_detail, name='chatbot_conversation_detail'),
    path('chatbot/conversation/<str:session_id>/delete/', delete_conversation, name='delete_conversation'),
    
    # Notificações
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/read-all/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    path('api/notifications/unread-count/', views.get_unread_count, name='get_unread_count'),
    
# Rotas do Marketplace
    path('marketplace/', include('marketplace.urls')),
]
