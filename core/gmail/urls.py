from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.initiate_auth, name='gmail-auth'),
    path('callback/', views.oauth_callback, name='gmail-callback'),
    path('status/', views.connection_status, name='gmail-status'),
    path('emails/', views.get_emails, name='gmail-emails'),
]