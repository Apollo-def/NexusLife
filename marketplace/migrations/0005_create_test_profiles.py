from django.db import migrations

def create_test_users(apps, schema_editor):
    from django.contrib.auth.hashers import make_password
    User = apps.get_model('auth', 'User')
    FreelancerProfile = apps.get_model('marketplace', 'FreelancerProfile')
    
    # PF user
    usuario, created1 = User.objects.get_or_create(
        username='usuario',
        defaults={
            'email': 'usuario@example.com',
            'first_name': 'Usuario',
            'last_name': 'PF',
            'is_active': True,
            'is_staff': False,
        }
    )
    usuario.password = make_password('usuario1234')
    usuario.save(update_fields=['password'])
    
    profile_pf, _ = FreelancerProfile.objects.get_or_create(user=usuario)
    profile_pf.person_type = 'PF'
    profile_pf.save()
    
    # PJ user
    empresa, created2 = User.objects.get_or_create(
        username='empresa',
        defaults={
            'email': 'empresa@example.com',
            'first_name': 'Empresa',
            'last_name': 'PJ',
            'is_active': True,
            'is_staff': False,
        }
    )
    empresa.password = make_password('empresa1234')
    empresa.save(update_fields=['password'])
    
    profile_pj, _ = FreelancerProfile.objects.get_or_create(user=empresa)
    profile_pj.person_type = 'PJ'
    profile_pj.business_name = 'Empresa Nexus'
    profile_pj.cnpj = '12.345.678/0001-99'
    profile_pj.state_registration = '123456789'
    profile_pj.save()

def reverse_func(apps, schema_editor):
    # Optional reverse, delete test users
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=['usuario', 'empresa']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('marketplace', '0004_freelancerprofile_state_registration'),
    ]

    operations = [
        migrations.RunPython(create_test_users, reverse_func),
    ]

