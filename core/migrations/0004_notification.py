# Generated migration for Notification model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='average_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='completion_rate',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_earnings',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='response_time',
            field=models.IntegerField(default=24, help_text='Tempo em horas'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_reviews',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='business_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cnpj',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('order', 'Novo Pedido'), ('order_updated', 'Pedido Atualizado'), ('review', 'Nova Avaliação'), ('message', 'Nova Mensagem'), ('payment', 'Pagamento'), ('account', 'Conta')], max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('icon', models.CharField(default='fas fa-bell', max_length=50)),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notificação',
                'verbose_name_plural': 'Notificações',
                'ordering': ['-created_at'],
            },
        ),
    ]
