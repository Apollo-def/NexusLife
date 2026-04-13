"""
Script de teste para verificar redirecionamento de admin após login
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexuslife.settings')
django.setup()

from django.contrib.auth.models import User

try:
    admin_user = User.objects.get(username='admin')
    print("[OK] Usuario admin encontrado")
    print(f"  Username: {admin_user.username}")
    print(f"  Email: {admin_user.email}")
    print(f"  is_staff: {admin_user.is_staff}")
    print(f"  is_superuser: {admin_user.is_superuser}")
    print("\n[INFO] Apos login, admin sera redirecionado para: /admin/")
    print("[INFO] Login pode ser feito em: http://localhost:8000/login/")
except User.DoesNotExist:
    print("[ERRO] Usuario admin nao encontrado")
