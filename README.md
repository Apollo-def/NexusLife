# NexusLife

Projeto Django criado com estrutura completa e sistema de autenticação.

## Estrutura do Projeto

```
NexusLife/
├── core/                    # App Django principal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # Formulários de autenticação
│   ├── models.py
│   ├── tests.py
│   ├── views.py            # Views de login/cadastro
│   ├── migrations/
│   └── templates/
│       └── core/
│           ├── base.html
│           ├── login.html
│           ├── register.html
│           └── home.html
├── nexuslife/               # Configurações do Projeto
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── app.py
├── db.sqlite3              # Banco de dados
└── README.md
```

## Funcionalidades

- **Login**: Sistema de autenticação de usuários
- **Cadastro**: Registro de novos usuários
- **Home**: Página inicial do sistema (protegida)
- **Logout**: Encerrar sessão

## Rotas

| URL | Descrição |
|-----|------------|
| `/` | Login |
| `/register/` | Cadastro de novo usuário |
| `/home/` | Página inicial (requer login) |
| `/logout/` | Encerrar sessão |
| `/admin/` | Painel administrativo |

## Comandos Úteis

| Comando | Descrição |
|---------|------------|
| `python manage.py runserver` | Iniciar o servidor de desenvolvimento |
| `python manage.py makemigrations` | Criar migrações |
| `python manage.py migrate` | Aplicar migrações |
| `python manage.py createsuperuser` | Criar super usuário |
| `python manage.py startapp nome_app` | Criar novo app |

## Como Rodar

```bash
# Instalar dependências (se necessário)
python -m pip install django==4.2

# Rodar o servidor
python manage.py runserver
```

O servidor estará disponível em: http://127.0.0.1:8000/

## Configurações

- **DEBUG**: True (desativar em produção)
- **Banco de Dados**: SQLite3 (db.sqlite3)
- **Idioma**: Inglês (en-us)
- **Fuso Horário**: UTC
