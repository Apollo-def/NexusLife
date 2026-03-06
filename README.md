# NexusLife

> Projeto Django com autenticação e integração Firebase.

## 📋 Descrição

NexusLife é uma aplicação web desenvolvida com Django que conta com sistema completo de autenticação de usuários, integrado com Firebase para提供了安全可靠的登录和注册功能。

## 🛠️ Tecnologias

| Tecnologia | Descrição |
|------------|------------|
| **Django 4.2** | Framework web Python de alto nível |
| **Python 3.x** | Linguagem de programação |
| **Firebase** | Backend como serviço (Auth, Database) |
| **SQLite** | Banco de dados leve para desenvolvimento |
| **HTML/CSS** | Interface do usuário |

## 📁 Estrutura do Projeto

```
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
│           ├── base.html        # Template base
│           ├── login.html       # Página de login
│           ├── register.html   # Página de cadastro
│           └── home.html       # Página inicial
├── nexuslife/                   # Configurações do Projeto
│   ├── __init__.py
│   ├── asgi.py                  # Configuração ASGI
│   ├── settings.py              # Configurações do Django
│   ├── urls.py                  # Rotas principais
│   └── wsgi.py                  # Configuração WSGI
├── static/                      # Arquivos estáticos
│   └── styles.css               # Estilos CSS
├── manage.py                    # Script de gerenciamento Django
├── requirements.txt            # Dependências do projeto
├── db.sqlite3                   # Banco de dados SQLite
└── README.md                    # Este arquivo
```

## ✨ Funcionalidades

### Autenticação
- ✅ **Login** - Sistema de autenticação de usuários
- ✅ **Cadastro** - Registro de novos usuários
- ✅ **Logout** - Encerrar sessão
- ✅ **Proteção de rotas** - Páginas restritas a usuários autenticados

### Integração Firebase
- 🔥 **Firebase Authentication** - Autenticação via Firebase
- 🔥 **Suporte a múltiplos provedores** - Email/Senha, Google, etc.
- 🔥 **Verificação de tokens JWT** - Segurança reforçada

### Usuário
- 🏠 **Home** - Página inicial personalizada
- 👤 **Perfil** - Gerenciamento de conta

## 🚀 Como Rodar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd NexusLife

# 2. Criar ambiente virtual (opcional mas recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar migrações
python manage.py migrate

# 5. Criar super usuário (opcional)
python manage.py createsuperuser

# 6. Rodar o servidor
python manage.py runserver
```

### Configuração do Firebase

1. Acesse o [Console do Firebase](https://console.firebase.google.com/)
2. Selecione o projeto **NexusLife**
3. Vá para **Configurações do projeto** (ícone de engrenagem)
4. Selecione **Contas de serviço**
5. Clique em **Gerar nova chave privada**
6. Salve o arquivo JSON na raiz do projeto como `firebase-credentials.json`

> ⚠️ **Importante**: Adicione `firebase-credentials.json` ao `.gitignore` para evitar exposing suas credenciais!

### Configuração do Firebase no Código

Edite o arquivo `core/firebase_config.py` e atualize as configurações:

```python
firebase_config = {
    "apiKey": "SUA_API_KEY",
    "authDomain": "nexuslife.firebaseapp.com",
    "projectId": "nexuslife",
    "storageBucket": "nexuslife.appspot.com",
    "messagingSenderId": "SEU_SENDER_ID",
    "appId": "SEU_APP_ID",
    "databaseURL": ""
}
```

## 📌 Rotas Disponíveis

| URL | Descrição | Acesso |
|-----|------------|--------|
| `/` | Login | Público |
| `/register/` | Cadastro de novo usuário | Público |
| `/home/` | Página inicial | Autenticado |
| `/logout/` | Encerrar sessão | Autenticado |
| `/admin/` | Painel administrativo | Admin |

## 📝 Comandos Úteis

| Comando | Descrição |
|---------|------------|
| `python manage.py runserver` | Iniciar servidor de desenvolvimento |
| `python manage.py makemigrations` | Criar migrações |
| `python manage.py migrate` | Aplicar migrações ao banco |
| `python manage.py createsuperuser` | Criar super usuário |
| `python manage.py startapp nome_app` | Criar novo app |
| `python manage.py test` | Executar testes |
| `python manage.py check` | Verificar erros no projeto |

## 🔧 Configurações do Projeto

As configurações principais estão em `nexuslife/settings.py`:

```python
DEBUG = True              # Desativar em produção
ALLOWED_HOSTS = []        # Adicionar domínios em produção
DATABASES = { ... }       # Configuração do banco de dados
SECRET_KEY = '...'        # Chave secreta (manter em segredo!)
```

## 📱 Acesso

O servidor estará disponível em: **http://127.0.0.1:8000/**

## 📄 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido com ❤️ usando Django e Firebase

