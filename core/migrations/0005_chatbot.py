# Generated migration for ChatbotConversation and ChatbotMessage models

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatbotConversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=100, unique=True)),
                ('title', models.CharField(blank=True, default='Conversa', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chatbot_conversations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Conversa Chatbot',
                'verbose_name_plural': 'Conversas Chatbot',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ChatbotMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(choices=[('user', 'Usuário'), ('bot', 'Bot')], max_length=10)),
                ('message', models.TextField()),
                ('tokens_used', models.IntegerField(default=0, help_text='Tokens de OpenAI usados')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.chatbotconversation')),
            ],
            options={
                'verbose_name': 'Mensagem Chatbot',
                'verbose_name_plural': 'Mensagens Chatbot',
                'ordering': ['created_at'],
            },
        ),
    ]
