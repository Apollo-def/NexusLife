from django.db import migrations


def create_sample_pj_services(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Category = apps.get_model('marketplace', 'Category')
    Service = apps.get_model('marketplace', 'Service')
    FreelancerProfile = apps.get_model('marketplace', 'FreelancerProfile')

    try:
        empresa = User.objects.get(username='empresa')
    except User.DoesNotExist:
        return

    pj_profile, _ = FreelancerProfile.objects.get_or_create(user=empresa)
    pj_profile.person_type = 'PJ'
    pj_profile.business_name = pj_profile.business_name or 'Empresa Nexus'
    pj_profile.cnpj = pj_profile.cnpj or '12.345.678/0001-99'
    pj_profile.state_registration = pj_profile.state_registration or '123456789'
    pj_profile.save()

    design_category, _ = Category.objects.get_or_create(
        name='Design',
        defaults={'description': 'Serviços de design gráfico, logos e identidade visual.'}
    )
    dev_category, _ = Category.objects.get_or_create(
        name='Desenvolvimento',
        defaults={'description': 'Serviços de desenvolvimento web e apps.'}
    )
    marketing_category, _ = Category.objects.get_or_create(
        name='Marketing Digital',
        defaults={'description': 'Serviços de marketing, redes sociais e SEO.'}
    )

    Service.objects.get_or_create(
        title='Criação de logotipo profissional',
        freelancer=empresa,
        defaults={
            'description': 'Design de logotipo exclusivo para sua empresa, entregue em vários formatos prontos para uso.',
            'price': '450.00',
            'category': design_category,
            'delivery_days': 5,
            'revisions': 3,
            'is_active': True,
        }
    )

    Service.objects.get_or_create(
        title='Desenvolvimento de landing page responsiva',
        freelancer=empresa,
        defaults={
            'description': 'Landing page rápida e responsiva para captação de leads e divulgação de serviços.',
            'price': '1200.00',
            'category': dev_category,
            'delivery_days': 7,
            'revisions': 2,
            'is_active': True,
        }
    )

    Service.objects.get_or_create(
        title='Gestão de redes sociais e conteúdo',
        freelancer=empresa,
        defaults={
            'description': 'Criação de conteúdo, planejamento de posts e análise de desempenho para redes sociais.',
            'price': '900.00',
            'category': marketing_category,
            'delivery_days': 10,
            'revisions': 2,
            'is_active': True,
        }
    )


def reverse_func(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Service = apps.get_model('marketplace', 'Service')

    try:
        empresa = User.objects.get(username='empresa')
        Service.objects.filter(freelancer=empresa, title__in=[
            'Criação de logotipo profissional',
            'Desenvolvimento de landing page responsiva',
            'Gestão de redes sociais e conteúdo'
        ]).delete()
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_alter_service_category_alter_service_created_at_and_more'),
    ]

    operations = [
        migrations.RunPython(create_sample_pj_services, reverse_func),
    ]
