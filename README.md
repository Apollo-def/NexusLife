# NexusLife

> Projeto Django com autenticação e integração Firebase.

##  Descrição

NexusLife é uma aplicação web desenvolvida com Django que conta com sistema completo de autenticação de usuários, integrado com Firebase para fornecer login e cadastro de forma segura.

##  Tecnologias

| Tecnologia | Descrição |
|------------|------------|
| **Django 4.2** | Framework web Python de alto nível |
| **Python 3.x** | Linguagem de programação |
| **PostgreSQL** | Banco de dados relacional utilizado para persistência |
| **Firebase** | Backend como serviço (Auth, Database) |
| **HTML/CSS** | Interface do usuário |

---

# 🗄️ Banco de Dados

O projeto utiliza **PostgreSQL** como banco de dados e a **ORM nativa do Django** para manipulação dos dados.

A configuração do banco está definida no arquivo:


nexuslife/settings.py


```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql','NAME': 'nexuslife',
        'USER': 'postgres',
        'PASSWORD': '1212',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

O modelo User foi criado no app core e gerou automaticamente a tabela:

core_user

no banco PostgreSQL após a execução das migrações.📁 Estrutura do Projeto
NexusLife/
├── core/                        # App Django principal
│   ├── __init__.py
│   ├── admin.py                 # Configuração do admin Django
│   ├── apps.py                  # Configurações do app
│   ├── forms.py                 # Formulários de autenticação
│   ├── models.py                # Modelos do banco de dados
│   ├── tests.py                 # Testes unitários
│   ├── views.py                 # Views de login/cadastro
│   ├── firebase_config.py       # Configuração do Firebase
│   ├── migrations/
│   └── templates/
│       └── core/
│           ├── base.html
│           ├── login.html
│           ├── register.html
│           └── home.html
├── nexuslife/                   # Configurações do Projeto
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   └── styles.css
├── manage.py
├── requirements.txt
└── README.md
 Funcionalidades

Autenticação

 Login de usuários

 Cadastro de novos usuários

 Logout

 Proteção de rotas

Integração Firebase

 Firebase Authentication

 Suporte a múltiplos provedores

 Verificação de tokens JWT

Usuário

 Página inicial

 Gerenciamento de conta

 Como Rodar o Projeto
Pré-requisitos

Python 3.8+

PostgreSQL instalado

pip

Instalação
# Clonar o repositório
git clone <url-do-repositorio>

cd NexusLife

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.\.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
Criar banco PostgreSQL

Você pode criar o banco usando pgAdmin ou terminal.

Exemplo via terminal:

createdb nexuslife

Ou criar manualmente no pgAdmin com o nome:

nexuslife
Executar migrações
python manage.py makemigrations
python manage.py migrate

Isso criará automaticamente as tabelas no banco PostgreSQL.

Criar super usuário (opcional)
python manage.py createsuperuser
Rodar o servidor
python manage.py runserver

A aplicação estará disponível em:

http://127.0.0.1:8000/



 Teste de Inserção via ORM

Exemplo usando o Django ORM:

from core.models import User

User.objects.create(
    name="Teste",
    email="teste@email.com",
    password="123456"
)

User.objects.all()

Isso insere um usuário na tabela:

core_user

 Rotas Disponíveis
URL	Descrição	Acesso
/	Login	Público
/register/	Cadastro	Público
/home/	Página inicial	Autenticado
/logout/	Logout	Autenticado
/admin/	Admin Django	Admin

 Comandos Úteis
Comando	Descrição
python manage.py runserver	Iniciar servidor
python manage.py makemigrations	Criar migrações
python manage.py migrate	Aplicar migrações
python manage.py createsuperuser	Criar admin
python manage.py startapp nome	Criar novo app
python manage.py test	Executar testes
🔧 Configurações do Projeto

Principais configurações no arquivo:

nexuslife/settings.py
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {...}
SECRET_KEY = '...'
Licença

Este projeto está sob licença MIT.