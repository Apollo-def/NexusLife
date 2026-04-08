#!/usr/bin/env python
"""
Script para testar os signals de notificações e emails.
Run com: python manage.py shell < test_signals.py
"""

from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Notification, UserProfile
from marketplace.models import Order, Service, Category, FreelancerProfile

# Criar usuário de teste se não existir
test_user, created = User.objects.get_or_create(
    username='test_user_signals',
    defaults={
        'email': 'test_signals@nexuslife.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

if created:
    test_user.set_password('TestPass123!')
    test_user.save()
    print(f"✅ Usuário criado: {test_user.username}")
else:
    print(f"✅ Usuário existente: {test_user.username}")

# Verificar se notificações foram criadas durante o registro
notifications = Notification.objects.filter(user=test_user)
print(f"\n📬 Notificações para {test_user.username}: {notifications.count()}")

# Listar todas as notificações
for notif in notifications:
    print(f"  - [{notif.notification_type}] {notif.message} ({notif.created_at.strftime('%H:%M:%S')})")

# Testar marcar como lida
if notifications.exists():
    first_notif = notifications.first()
    print(f"\n📌 Marcando notificação como lida: {first_notif.message}")
    first_notif.mark_as_read()
    print(f"✅ Notificação marcada como lida em {first_notif.read_at}")

print("\n✅ Testes completados!")
