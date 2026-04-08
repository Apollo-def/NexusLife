from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .models import Notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_notification_on_user_registration(sender, instance, created, **kwargs):
    """Cria notificação quando usuário se registra"""
    if created:
        try:
            # Criar notificação bem-vindo
            Notification.objects.create(
                user=instance,
                notification_type='account',
                title='Bem-vindo ao NexusLife!',
                message='Sua conta foi criada com sucesso. Comece explorando o marketplace!',
                icon='fas fa-check-circle',
                link='/marketplace/'
            )
            
            # Enviar email de boas-vindas
            send_welcome_email(instance)
            logger.info(f"Notificação e email enviados para {instance.email}")
        except Exception as e:
            logger.error(f"Erro ao criar notificação: {str(e)}")


def send_welcome_email(user):
    """Envia email de boas-vindas"""
    try:
        context = {
            'user_name': user.first_name or user.username,
            'username': user.username,
            'site_url': settings.SITE_URL,
        }
        
        html_message = render_to_string('emails/welcome.html', context)
        subject = f'Bem-vindo ao NexusLife, {user.first_name or user.username}!'
        
        send_mail(
            subject=subject,
            message='Bem-vindo ao NexusLife!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email de boas-vindas enviado para {user.email}")
    except Exception as e:
        logger.error(f"Erro ao enviar email: {str(e)}")


def send_order_notification(order):
    """Envia notificação de novo pedido"""
    try:
        # Notificar freelancer
        if hasattr(order, 'service') and order.service.freelancer:
            Notification.objects.create(
                user=order.service.freelancer,
                notification_type='order',
                title=f'Novo pedido: {order.service.title}',
                message=f'Você recebeu um novo pedido de {order.client.username}',
                icon='fas fa-shopping-cart',
                link=f'/marketplace/order/{order.pk}/'
            )
            
            # Email para freelancer
            send_order_email(
                order.service.freelancer,
                order,
                email_type='new_order'
            )
        
        # Notificar cliente
        Notification.objects.create(
            user=order.client,
            notification_type='order',
            title='Pedido criado com sucesso',
            message=f'Seu pedido para {order.service.title} foi enviado',
            icon='fas fa-check-circle',
            link=f'/marketplace/order/{order.pk}/'
        )
        
        logger.info(f"Notificações de pedido criadas: {order.pk}")
    except Exception as e:
        logger.error(f"Erro ao enviar notificação de pedido: {str(e)}")


def send_order_email(user, order, email_type='new_order'):
    """Envia email relacionado a pedidos"""
    try:
        context = {
            'user_name': user.first_name or user.username,
            'order': order,
            'service': order.service,
            'site_url': settings.SITE_URL,
        }
        
        if email_type == 'new_order':
            html_message = render_to_string('emails/new_order.html', context)
            subject = f'Novo Pedido: {order.service.title}'
        elif email_type == 'order_accepted':
            html_message = render_to_string('emails/order_accepted.html', context)
            subject = 'Pedido Aceito'
        elif email_type == 'order_completed':
            html_message = render_to_string('emails/order_completed.html', context)
            subject = 'Pedido Concluído'
        else:
            return
        
        send_mail(
            subject=subject,
            message='Notificação do NexusLife',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email de pedido ({email_type}) enviado para {user.email}")
    except Exception as e:
        logger.error(f"Erro ao enviar email de pedido: {str(e)}")


def send_review_notification(review):
    """Envia notificação de avaliação"""
    try:
        # Notificar freelancer que recebeu avaliação
        if hasattr(review, 'freelancer'):
            Notification.objects.create(
                user=review.freelancer.user,
                notification_type='review',
                title=f'Nova avaliação: {review.rating} estrelas',
                message=f'{review.reviewer.username} avaliou seu trabalho',
                icon='fas fa-star',
                link=f'/profile/'
            )
            
            send_review_email(review.freelancer.user, review)
        
        logger.info(f"Notificação de avaliação criada: {review.pk}")
    except Exception as e:
        logger.error(f"Erro ao enviar notificação de avaliação: {str(e)}")


def send_review_email(user, review):
    """Envia email de nova avaliação"""
    try:
        context = {
            'user_name': user.first_name or user.username,
            'review': review,
            'site_url': settings.SITE_URL,
        }
        
        html_message = render_to_string('emails/new_review.html', context)
        subject = f'Você recebeu uma avaliação: {review.rating} estrelas'
        
        send_mail(
            subject=subject,
            message='Você recebeu uma nova avaliação',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email de avaliação enviado para {user.email}")
    except Exception as e:
        logger.error(f"Erro ao enviar email de avaliação: {str(e)}")
