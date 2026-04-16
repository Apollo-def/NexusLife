<div align="center">

<img src="static/images/logo.png" alt="NexusLife Logo" width="120"/>

# <i class="fas fa-rocket"></i> NexusLife

**Marketplace de Serviços Digitais - Plataforma Full-Stack com Django + React**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14-A30000?style=flat-square&logo=django&logoColor=white)](https://www.django-rest-framework.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

</div>

---

## <i class="fas fa-clipboard-list"></i> Descrição

**NexusLife** é uma plataforma profissional de marketplace para serviços digitais, conectando freelancers com clientes. Sistema completo com:

<i class="fas fa-star"></i> **Recursos Principais:**
- <i class="fas fa-lock"></i> Autenticação completa (Django Auth + Firebase opcional)
- <i class="fas fa-briefcase"></i> Perfil de freelancer com histórico e avaliações
- <i class="fas fa-shopping-cart"></i> Catálogo de serviços com filtros avançados
- <i class="fas fa-star-half-alt"></i> Sistema de avaliações e ratings
- <i class="fas fa-money-bill-wave"></i> Gestão de pedidos e transações
- <i class="fas fa-heart"></i> Sistema de favoritos/bookmarks
- <i class="fas fa-chart-bar"></i> Dashboard para clientes e freelancers
- <i class="fas fa-palette"></i> Interface moderna e responsiva
- <i class="fas fa-rocket"></i> REST API completa com DRF

**Público-alvo:** Empreendedores, agências, e startups que querem uma plataforma de serviços pronta para uso ou customização.

---

## <i class="fas fa-bolt"></i> Quick Start

### <i class="fas fa-code-branch"></i> Clone e Instale

```bash
# Clone o repositório
git clone <repository-url> NexusLife
cd NexusLife

# Crie virtual environment
python -m venv venv

# Ative (Windows)
venv\Scripts\activate
# Ou (macOS/Linux)
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### <i class="fas fa-database"></i> Configure o Banco de Dados

```bash
# Crie migrações
python manage.py makemigrations

# Aplique migrações
python manage.py migrate

# Crie super usuário (admin)
python manage.py createsuperuser
# Será solicitado username, email, e senha
```

### <i class="fas fa-play"></i> Inicie o Servidor

```bash
# Backend (Django)
python manage.py runserver

# Frontend (outro terminal)
cd frontend
npm run dev
```

### <i class="fas fa-globe"></i> Acesse

| Recurso | URL | Status |
|---------|-----|--------|
| <i class="fas fa-home"></i> Frontend | `http://localhost:5173` | <i class="fas fa-check-circle text-success"></i> Conectado |
| <i class="fas fa-tools"></i> Admin Django | `http://localhost:8000/admin` | <i class="fas fa-check-circle text-success"></i> Conectado |
| <i class="fas fa-broadcast-tower"></i> API Rest | `http://localhost:8000/api` | <i class="fas fa-check-circle text-success"></i> Conectado |

---

## <i class="fas fa-key"></i> Credenciais de Acesso

### <i class="fas fa-shield-alt"></i> Admin Django

**URL:** `http://localhost:8000/admin`

**Credenciais Padrão (crie a sua):**
```
Username: admin
Senha: <define durante createsuperuser>
Email: admin@nexuslife.com
```

> **Primeira vez?** Execute: `python manage.py createsuperuser`

### 📡 API Endpoints

**Base URL:** `http://localhost:8000/marketplace/api/`

#### Categorias
```
GET /categories/              - Listar categorias
```

#### Serviços
```
GET    /services/             - Listar serviços com filtros
POST   /services/             - Criar novo serviço
GET    /services/{id}/        - Ver detalhes
PUT    /services/{id}/        - Atualizar
DELETE /services/{id}/        - Deletar
GET    /services/my_services/ - Meus serviços
GET    /services/reviews/     - Ver avaliações
```

#### Perfil Freelancer
```
GET    /freelancer-profiles/        - Listar perfis
POST   /freelancer-profiles/        - Criar perfil
GET    /freelancer-profiles/me/     - Meu perfil
PUT    /freelancer-profiles/me/     - Atualizar
```

#### Pedidos
```
POST   /orders/              - Criar pedido
GET    /orders/my_orders/    - Meus pedidos (cliente)
GET    /orders/incoming_orders/ - Pedidos recebidos (freelancer)
POST   /orders/{id}/update_status/ - Atualizar status
```

#### Avaliações
```
GET    /reviews/              - Listar todas
GET    /reviews/by_freelancer/ - Por freelancer
POST   /orders/{id}/review/   - Criar avaliação
```

#### Favoritos
```
GET    /favorites/            - Meus favoritos
POST   /favorites/add/        - Adicionar
POST   /favorites/remove/     - Remover
```

---

## <i class="fas fa-folder-open"></i> Estrutura do Projeto

```
NexusLife/
├── nexuslife/                   # Configuração geral Django
│   ├── settings.py              # Configurações (BD, apps, etc)
│   ├── urls.py                  # URLs principais
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                        # App de usuários e autenticação
│   ├── models.py                # User model customizado
│   ├── views.py                 # Autenticação views
│   ├── forms.py                 # Formulários
│   ├── urls.py                  # URLs da auth
│   ├── admin.py
│   ├── templates/
│   │   └── core/
│   │       ├── base.html        # Template base
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── profile.html
│   │       └── password_reset.html
│   ├── migrations/
│   └── __init__.py
│
├── marketplace/                 # App do marketplace (novo!)
│   ├── models.py                # 6 modelos: Service, Order, Review, etc
│   ├── serializers.py           # Serializers DRF
│   ├── api.py                   # ViewSets e endpoints
│   ├── views.py
│   ├── urls.py
│   ├── admin.py                 # Admin interface completo
│   ├── permissions.py
│   ├── filters.py
│   ├── migrations/
│   └── __init__.py
│
├── frontend/                    # React + TypeScript
│   ├── src/
│   │   ├── components/
│   │   │   ├── FeaturesSection.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Header.tsx
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── ServiceList.tsx
│   │   │   ├── ServiceDetail.tsx
│   │   │   ├── FreelancerProfile.tsx
│   │   │   ├── FreelancerDashboard.tsx
│   │   │   ├── ClientDashboard.tsx
│   │   │   ├── OrderDetail.tsx
│   │   │   └── CreateService.tsx
│   │   ├── App.tsx              # Rotas
│   │   └── main.tsx
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── static/                      # Arquivos estáticos
│   ├── styles.css               # CSS global (melhorado)
│   ├── main.js                  # JavaScript interativo
│   ├── images/
│   └── ...
│
├── db.sqlite3                   # Banco (desenvolvimento)
├── requirements.txt             # Dependências Python
├── manage.py                    # CLI Django
├── firebase-credentials.json    # Credenciais Firebase (opcional)
├── .env                         # Variáveis de ambiente
├── README.md                    # Este arquivo
└── TODO.md                      # Tarefas pendentes
```

---

## <i class="fas fa-wrench"></i> Tecnologias Utilizadas

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework 3.14** - REST API
- **PostgreSQL/SQLite** - Banco de dados
- **Pillow** - Processamento de imagens
- **django-cors-headers** - CORS

### Frontend
- **React 18** - Interface
- **TypeScript 5** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - Componentes
- **React Router** - Roteamento

### Deploy Ready
- Docker (opcional)
- PostgreSQL (produção)
- Gunicorn WSGI
- Nginx (reverse proxy)

---

## <i class="fas fa-database"></i> Modelos de Dados

### Categoria
- `name` - Nome da categoria
- `description` - Descrição
- `icon` - Ícone

### Service
- `title` - Título do serviço
- `description` - Descrição detalhada
- `price` - Preço em R$
- `category` - FK para Categoria
- `freelancer` - FK para User
- `delivery_days` - Prazo de entrega
- `revisions` - Número de revisões
- `is_active` - Ativo/Inativo
- `average_rating` - Calculado
- `total_orders` - Contado

### Order
- `service` - FK para Service
- `client` - FK para User (cliente)
- `status` - pending/in_progress/completed/cancelled/disputed
- `amount` - Valor da transação
- `completed_at` - Data de conclusão
- `notes` - Anotações

### Review
- `order` - OneToOne para Order
- `service` - FK para Service
- `reviewer` - FK para User
- `rating` - 1-5 stars
- `comment` - Comentário

### Favorite
- `user` - FK para User
- `service` - FK para Service
- `unique_together` - (user, service)

### FreelancerProfile
- `user` - OneToOne para User
- `bio` - Biografia
- `profile_image` - Foto
- `hourly_rate` - Taxa horária
- `location` - Localização
- `phone` - Telefone
- `website` - Website pessoal
- `verified` - Verificado?
- `response_time` - Tempo de resposta
- `total_earnings` - Ganhos totais
- `average_rating` - Calculado
- `completion_rate` - Calculado

---

## 🔧 Autenticação

### 1. Login/Register
```bash
# Página de login
GET http://localhost:8000/

# Página de registro
GET http://localhost:8000/register/

# API de autenticação
POST /api/auth/login/
POST /api/auth/register/
```

### 2. Permissões
- `IsAuthenticated` - Apenas usuários logados
- `IsOwner` - Apenas proprietário do recurso
- `IsFreelancer` - Apenas freelancers
- `IsClient` - Apenas clientes

### 3. JWT (Opcional)
```python
# Token format
Authorization: Bearer <token>

# Gerado no login, válido por 24h
```

---

## 📝 Guias Adicionais

### Criar Service via Admin
1. Acesse `http://localhost:8000/admin/marketplace/service/add/`
2. Preencha dados
3. Clique em "Save"

### Criar Categoria
1. No admin, acesse `Marketplace > Categories`
2. Clique em "Add Category"
3. Preencha nome, descrição, ícone

### Usuários e Permissões
1. Admin: `http://localhost:8000/admin/auth/user/`
2. Dê permissões via Django admin
3. Atribua grupos de usuários

---

## <i class="fas fa-rocket"></i> Deployment

### Heroku
```bash
heroku create nexuslife
git push heroku main
heroku run python manage.py migrate
```

### AWS EC2
```bash
# SSH e configure
ssh -i key.pem ubuntu@instance

# Clone e setup
git clone <url> NexusLife
cd NexusLife
./deploy.sh
```

### Docker
```bash
docker build -t nexuslife .
docker run -p 8000:8000 nexuslife
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

**Encontrou um bug?** Abra uma issue no GitHub!

**Precisa de ajuda?** Confira a documentação ou contate-nos:
- 📧 Email: support@nexuslife.com
- 💬 Discord: [Comunidade NexusLife]()
- 📖 Docs: [https://nexuslife.docs.io]()

[Logout]   → Encerra sessão Django e redireciona para /login

[Reset]    → Envia e-mail de redefinição via Firebase Auth
```

### Rotas disponíveis

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/` | Página de login | Público |
| `/register/` | Cadastro de novo usuário | Público |
| `/home/` | Dashboard principal | Autenticado |
| `/profile/` | Edição de perfil | Autenticado |
| `/logout/` | Encerrar sessão | Autenticado |
| `/password-reset/` | Redefinição de senha | Público |
| `/admin/` | Painel administrativo Django | Admin |

---

## Funcionalidades

### Autenticação
- Login com username, e-mail ou CPF
- Cadastro com validação de formulário (Django Forms)
- Logout com redirecionamento configurável
- Proteção de rotas com `@login_required`
- Redirecionamentos automáticos pós-login/logout via `settings.py`

### Integração Firebase
- Criação de usuário no Firebase Authentication no momento do cadastro
- Envio automático de e-mail de verificação
- Redefinição de senha via Firebase (sem SMTP próprio)
- Armazenamento de dados de perfil no Firestore (`users/{uid}`)
- Verificação de tokens JWT via Firebase Admin SDK
- Inicialização segura com degradação graciosa (sem crash se credenciais ausentes)

### Perfil de Usuário
- Atualização de nome, sobrenome e e-mail
- Formulário com validação server-side

### Frontend (SPA)
- Landing page com seções: Hero, Features, How It Works, Footer
- Roteamento com React Router DOM v6
- Gerenciamento de estado assíncrono com TanStack Query
- Componentes acessíveis via Radix UI (shadcn/ui)
- Tema claro/escuro com `next-themes`
- Testes com Vitest + Testing Library + Playwright (E2E)

---


## Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.8+ | Linguagem principal |
| Django | 4.2.x | Framework web, ORM, autenticação, admin |
| PostgreSQL | 13+ | Banco de dados relacional |
| psycopg2-binary | 2.9.x | Driver Python para PostgreSQL |
| python-decouple | 3.8 | Gerenciamento de variáveis de ambiente via `.env` |
| firebase-admin | 6.2.0 | SDK servidor: Firestore, verificação de tokens JWT |
| pyrebase4 | 4.9.0 | SDK cliente: criar usuário, login, reset de senha |

### Frontend
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| React | 18 | UI declarativa baseada em componentes |
| TypeScript | 5 | Tipagem estática |
| Vite | 5 | Build tool e dev server ultrarrápido |
| Tailwind CSS | 3 | Estilização utility-first |
| shadcn/ui + Radix UI | — | Componentes acessíveis e sem estilo imposto |
| React Router DOM | 6 | Roteamento client-side |
| TanStack Query | 5 | Cache e sincronização de dados assíncronos |
| React Hook Form + Zod | — | Formulários com validação de schema |
| Vitest + Playwright | — | Testes unitários e E2E |

### Infraestrutura
| Serviço | Uso |
|---------|-----|
| Firebase Authentication | Autenticação de usuários |
| Cloud Firestore | Armazenamento de dados de perfil |
| Firebase Console | Gerenciamento de credenciais e usuários |

---

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 13+ instalado e em execução
- Node.js 18+ e npm (ou bun)
- Conta no [Firebase](https://console.firebase.google.com) com um projeto criado
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/Apollo-def/NexusLife.git
cd NexusLife
```

### 2. Configurar o backend (Django)

```bash
# Criar e ativar ambiente virtual
python -m venv .venv

# Windows (PowerShell) — se necessário, habilite scripts primeiro:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# Instalar dependências Python
pip install -r requirements.txt
```

### 3. Criar o banco de dados PostgreSQL

Crie o banco via `psql` ou pgAdmin com o nome `nexuslife`:

```sql
CREATE DATABASE nexuslife;
```

### 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env` com seus valores:

```env
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=nexuslife
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

> O arquivo `.env` já está no `.gitignore` — nunca será enviado ao repositório.

### 5. Configurar o Firebase

1. Acesse o [Firebase Console](https://console.firebase.google.com)
2. Crie um projeto (ou use um existente)
3. Ative **Authentication** > **Email/Password**
4. Ative o **Cloud Firestore**
5. Vá em **Configurações do projeto** > **Contas de serviço** > **Gerar nova chave privada**
6. Salve o arquivo JSON baixado como `firebase-credentials.json` na raiz do projeto

> ⚠️ Nunca versione o `firebase-credentials.json`. Ele já está no `.gitignore`.

### 6. Configurar variáveis do Pyrebase

Edite `core/firebase_config.py` e substitua os valores de `firebase_config` com os dados do seu projeto:

```python
firebase_config = {
    "apiKey": "SUA_API_KEY",
    "authDomain": "seu-projeto.firebaseapp.com",
    "projectId": "seu-projeto",
    "storageBucket": "seu-projeto.appspot.com",
    "messagingSenderId": "SEU_SENDER_ID",
    "appId": "SEU_APP_ID",
    "databaseURL": "",
}
```

Você encontra esses valores em: **Firebase Console** > **Configurações do projeto** > **Geral** > **Seus apps** > ícone `</>`

### 7. Executar migrações e iniciar o servidor

```bash
python manage.py makemigrations
python manage.py migrate

# (Opcional) Criar superusuário para acessar /admin
python manage.py createsuperuser

# Iniciar servidor de desenvolvimento
python manage.py runserver
```

A aplicação estará disponível em: `http://127.0.0.1:8000/`

### 8. Configurar o frontend (opcional)

```bash
cd frontend
npm install

# Iniciar dev server do frontend
npm run dev
```

O frontend estará disponível em: `http://localhost:5173/`

---

## Uso

### Cadastro de usuário

Acesse `http://127.0.0.1:8000/register/` e preencha o formulário com:
- Username
- Nome e sobrenome
- E-mail
- CPF (opcional)
- Senha (mínimo 6 caracteres, validado pelo Django e Firebase)

Após o cadastro, um e-mail de verificação é enviado automaticamente.

### Login

Acesse `http://127.0.0.1:8000/` e faça login com:
- Username **ou** e-mail **ou** CPF + senha

Existem dois tipos de personas:
- **Pessoa Física (PF)**: use dados pessoais e CPF.
- **Pessoa Jurídica (PJ)**: use CNPJ e informações de empresa (business_name) criadas no perfil.

O perfil PF/PJ altera a experiência no dashboard (`home`) e na criação de serviços.

Para administração da plataforma (admin Django):
- Acesse `http://127.0.0.1:8000/admin/`
- Login separado de superusuário (criado com `python manage.py createsuperuser`)

### Redefinição de senha

Acesse `/password-reset/`, informe o e-mail cadastrado e um link de redefinição será enviado via Firebase.

### Uso via Django Shell

```python
python manage.py shell

from django.contrib.auth.models import User

# Listar todos os usuários
User.objects.all()

# Buscar por e-mail
User.objects.get(email="usuario@exemplo.com")

# Criar usuário programaticamente
user = User.objects.create_user(
    username="joao",
    email="joao@exemplo.com",
    password="senha_segura_123",
    first_name="João",
    last_name="Silva"
)
```

---

## Estrutura do Projeto

```
nexuslife/
├── core/                          # App Django principal
│   ├── migrations/                # Migrações do banco de dados
│   ├── templates/
│   │   └── core/
│   │       ├── base.html          # Template base (navbar, mensagens, Bootstrap)
│   │       ├── login.html         # Página de login
│   │       ├── register.html      # Página de cadastro
│   │       ├── home.html          # Dashboard (rota protegida)
│   │       ├── profile.html       # Edição de perfil
│   │       └── password_reset.html
│   ├── admin.py                   # Registro de modelos no admin Django
│   ├── apps.py                    # Configuração do app (inicializa Firebase no ready())
│   ├── firebase_config.py         # Inicialização Firebase Admin + Pyrebase
│   ├── forms.py                   # UserRegisterForm, LoginForm, UserUpdateForm
│   ├── models.py                  # Modelo User customizado (core_user)
│   ├── views.py                   # login, register, profile, home, logout, password_reset
│   └── tests.py                   # Testes automatizados
│
├── frontend/                      # SPA React + TypeScript (desacoplada)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                # Componentes shadcn/ui (50+ componentes Radix)
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── HeroSection.tsx
│   │   │   ├── FeaturesSection.tsx
│   │   │   └── HowItWorksSection.tsx
│   │   ├── pages/
│   │   │   ├── Index.tsx          # Landing page
│   │   │   └── NotFound.tsx       # Página 404
│   │   ├── hooks/                 # Hooks customizados (use-mobile, use-toast)
│   │   ├── lib/utils.ts           # Utilitários (cn helper para Tailwind)
│   │   ├── App.tsx                # Roteamento principal
│   │   └── main.tsx               # Entry point React
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── vite.config.ts
│   └── playwright.config.ts
│
├── nexuslife/                     # Configurações do projeto Django
│   ├── __init__.py
│   ├── settings.py                # Configurações gerais, DB (PostgreSQL), auth redirects
│   ├── urls.py                    # URLconf raiz
│   ├── wsgi.py
│   └── asgi.py
│
├── static/
│   ├── images/                    # Assets estáticos (logo, avatares)
│   └── styles.css                 # CSS global customizado
│
├── firebase-credentials.json      # ⚠️ NÃO versionar (está no .gitignore)
├── manage.py
└── requirements.txt
```

---

## Configuração

### Variáveis importantes em `nexuslife/settings.py`

| Variável | Valor atual | Descrição |
|----------|-------------|-----------|
| `SECRET_KEY` | `django-insecure-...` | Chave criptográfica — **troque em produção** |
| `DEBUG` | `True` | Desative em produção (`False`) |
| `ALLOWED_HOSTS` | `[]` | Adicione seu domínio em produção |
| `DATABASES` | PostgreSQL (`nexuslife`) | Banco de dados ativo |
| `LOGIN_URL` | `'login'` | Rota para usuários não autenticados |
| `LOGIN_REDIRECT_URL` | `'home'` | Rota após login bem-sucedido |
| `LOGOUT_REDIRECT_URL` | `'login'` | Rota após logout |

### Banco de dados (PostgreSQL)

O projeto usa PostgreSQL como banco de dados. A configuração atual em `nexuslife/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nexuslife',
        'USER': 'postgres',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configuração para PostgreSQL (produção)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nexuslife',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Instale o driver: `pip install psycopg2-binary`

### Variáveis de ambiente recomendadas (produção)

Crie um arquivo `.env` na raiz e use `python-decouple` ou `django-environ`:

```env
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DB_NAME=nexuslife
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

---

## Testes

### Backend (Django)

```bash
# Rodar todos os testes
python manage.py test

# Rodar testes de um app específico
python manage.py test core

# Com verbosidade
python manage.py test --verbosity=2
```

### Frontend (Vitest)

```bash
cd frontend

# Execução única (CI)
npm run test

# Modo watch (desenvolvimento)
npm run test:watch
```

### E2E (Playwright)

```bash
cd frontend

# Instalar browsers (primeira vez)
npx playwright install

# Rodar testes E2E
npx playwright test

# Com interface visual
npx playwright test --ui
```

---

## Deploy

### Pré-requisitos de produção

1. Defina `DEBUG=False` e configure `ALLOWED_HOSTS`
2. Troque a `SECRET_KEY` por uma chave forte e aleatória
3. Configure um banco PostgreSQL
4. Execute `python manage.py collectstatic`
5. Use um servidor WSGI como **Gunicorn** + **Nginx**

### Deploy com Gunicorn

```bash
pip install gunicorn

# Iniciar servidor WSGI
gunicorn nexuslife.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Deploy do frontend

```bash
cd frontend

# Gerar build de produção
npm run build

# Os arquivos estáticos estarão em frontend/dist/
# Sirva com Nginx ou hospede em Vercel/Netlify
```

### Plataformas suportadas

| Plataforma | Backend | Frontend |
|------------|---------|----------|
| Railway | <i class="fas fa-check-circle text-success"></i> | — |
| Render | <i class="fas fa-check-circle text-success"></i> | <i class="fas fa-check-circle text-success"></i> |
| Heroku | <i class="fas fa-check-circle text-success"></i> | — |
| Vercel | — | <i class="fas fa-check-circle text-success"></i> |
| Netlify | — | <i class="fas fa-check-circle text-success"></i> |
| VPS (Ubuntu + Nginx) | <i class="fas fa-check-circle text-success"></i> | <i class="fas fa-check-circle text-success"></i> |

---

## Contribuição

Contribuições são bem-vindas. Siga o fluxo abaixo:

### 1. Fork e clone

```bash
git clone https://github.com/seu-usuario/nexuslife.git
cd nexuslife
```

### 2. Crie uma branch

```bash
git checkout -b feat/nome-da-funcionalidade
# ou
git checkout -b fix/descricao-do-bug
```

### 3. Padrões de código

- **Python:** siga PEP 8. Use `flake8` ou `ruff` para lint.
- **TypeScript/React:** siga as regras do ESLint configurado (`eslint.config.js`).
- **Commits:** use [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat:` nova funcionalidade
  - `fix:` correção de bug
  - `docs:` documentação
  - `refactor:` refatoração sem mudança de comportamento
  - `test:` adição ou correção de testes

### 4. Abra um Pull Request

- Descreva claramente o que foi feito e por quê
- Referencie issues relacionadas (`Closes #123`)
- Certifique-se de que os testes passam antes de abrir o PR

---

## Roadmap

- [ ] Autenticação social (Google, GitHub) via Firebase
- [ ] Upload de foto de perfil com Firebase Storage
- [ ] Dashboard com métricas de usuário
- [ ] API REST com Django REST Framework
- [ ] Integração completa frontend React ↔ backend Django
- [ ] Suporte a 2FA (autenticação de dois fatores)
- [ ] Internacionalização (i18n) — pt-BR e en-US
- [ ] Containerização com Docker + docker-compose
- [ ] CI/CD com GitHub Actions

---

## FAQ

**O servidor inicia mesmo sem o `firebase-credentials.json`?**
Sim. O Firebase Admin é inicializado com degradação graciosa — se o arquivo não for encontrado ou estiver corrompido, um aviso é exibido no console e o servidor continua funcionando. As funcionalidades que dependem do Firebase Admin (Firestore, verificação de token) ficam desabilitadas, mas login/logout via Django funcionam normalmente.

**Preciso do PostgreSQL instalado para rodar o projeto?**
Sim. O projeto usa PostgreSQL como banco de dados. Certifique-se de ter o PostgreSQL instalado, o banco `nexuslife` criado e o serviço em execução antes de rodar as migrações.

**Posso usar SQLite em vez de PostgreSQL?**
Sim, para desenvolvimento rápido. Substitua o bloco `DATABASES` no `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**O frontend React é obrigatório?**
Não. O backend Django possui seus próprios templates HTML (Bootstrap 5) e funciona de forma completamente independente. O frontend é uma SPA separada para quem quiser evoluir o projeto para uma arquitetura desacoplada.

**Como adicionar novos campos ao perfil do usuário?**
Estenda o `UserUpdateForm` em `core/forms.py` e atualize a view `profile_view` em `core/views.py`. Para campos extras além do modelo `User` padrão do Django, crie um modelo `Profile` com `OneToOneField(User)`.

**Como proteger uma nova view?**
Adicione o decorator `@login_required` acima da função de view. Usuários não autenticados serão redirecionados para `LOGIN_URL` definido no `settings.py`.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## Autor

Desenvolvido com dedicação.

Para dúvidas, sugestões ou contribuições, abra uma [issue](https://github.com/seu-usuario/nexuslife/issues) ou envie um pull request.

---

## Integração OAuth Gmail

### O que foi implementado

A integração OAuth Gmail permite que usuários conectem suas contas Gmail à aplicação NexusLife de forma segura, sem compartilhar suas senhas. A aplicação pode então acessar e-mails do usuário com permissão explícita.

### Fluxo OAuth Gmail

```
1. Usuário clica em "Conectar Gmail"
   ↓
2. Redireciona para: http://localhost:8000/api/gmail/auth/
   ↓
3. Código redireciona para Google OAuth Consent Screen
   ↓
4. Google pede permissão ao usuário (ler e modificar Gmail)
   ↓
5. Usuário autoriza
   ↓
6. Google redireciona para: http://localhost:8000/api/gmail/callback/?code=XXXXX
   ↓
7. Código troca o "code" por um "access_token" e "refresh_token"
   ↓
8. Tokens são salvos no banco de dados (modelo GmailToken)
   ↓
9. Usuário é redirecionado para o perfil
```

### Arquivos criados/modificados

#### **core/gmail/models.py** - Armazena tokens OAuth
```python
class GmailToken(models.Model):
    user = ForeignKey(User)           # Qual usuário
    access_token = CharField()        # Token para acessar Gmail API
    refresh_token = CharField()       # Token para renovar acesso
    expires_at = DateTimeField()      # Quando o token expira
    email = CharField()               # Email do Gmail conectado
    is_active = BooleanField()        # Se a conexão está ativa
```

#### **core/gmail/views.py** - Controla o fluxo OAuth
Implementa 4 endpoints principais:

1. **`initiate_auth`** - Inicia o fluxo OAuth
   - Redireciona o usuário para o Google OAuth Consent Screen
   - Solicita permissões: `gmail.readonly` e `gmail.modify`

2. **`oauth_callback`** - Recebe o código do Google
   - Troca o código por tokens de acesso
   - Decodifica o ID token para obter o email do usuário
   - Salva os tokens no banco de dados

3. **`connection_status`** - Verifica status da conexão
   - Retorna se o Gmail está conectado
   - Mostra qual email está conectado

4. **`get_emails`** - Recupera emails não lidos
   - Usa o token para acessar a Gmail API
   - Retorna lista de emails não lidos

#### **core/gmail/services.py** - Comunica com Gmail API
```python
class GmailService:
    def get_unread_messages(max_results=10)  # Busca emails não lidos
    def test_connection()                     # Testa se a conexão funciona
```

#### **core/gmail/urls.py** - Define as rotas
```
/api/gmail/auth/       → Inicia OAuth (redireciona para Google)
/api/gmail/callback/   → Recebe resposta do Google
/api/gmail/status/     → Verifica status da conexão
/api/gmail/emails/     → Recupera emails não lidos
```

### Configuração do Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Vá para **APIs & Services** → **Credentials**
3. Crie uma credencial OAuth 2.0 do tipo "Aplicativo da Web"
4. Configure o **Authorized redirect URI**: `http://localhost:8000/api/gmail/callback/`
5. Copie o **Client ID** e **Client Secret**
6. Adicione seu email como usuário de teste em **OAuth consent screen** → **Test users**

### Variáveis de ambiente necessárias

Adicione ao `.env`:
```env
GOOGLE_CLIENT_ID=seu_client_id_aqui
GOOGLE_CLIENT_SECRET=seu_client_secret_aqui
GOOGLE_REDIRECT_URI=http://localhost:8000/api/gmail/callback/
```

### Como usar

**Para conectar Gmail:**
```
1. Faça login na aplicação
2. Acesse: http://localhost:8000/api/gmail/auth/
3. Autorize o acesso no Google
4. Pronto! Token salvo no banco de dados
```

**Para verificar status:**
```bash
curl http://localhost:8000/api/gmail/status/
# Retorna: {"connected": true, "email": "usuario@gmail.com", ...}
```

**Para recuperar emails:**
```bash
curl http://localhost:8000/api/gmail/emails/
# Retorna: {"success": true, "emails": [...]}
```

### Segurança

- <i class="fas fa-check-circle text-success"></i> Senha do usuário nunca é armazenada
- <i class="fas fa-check-circle text-success"></i> Tokens são armazenados no banco de dados PostgreSQL
- <i class="fas fa-check-circle text-success"></i> Tokens podem ser renovados automaticamente
- <i class="fas fa-check-circle text-success"></i> Tokens podem ser revogados a qualquer momento
- <i class="fas fa-check-circle text-success"></i> Acesso protegido por `@login_required`

### Próximos passos (opcional)

- Adicionar botão na interface para conectar Gmail
- Mostrar emails na página de perfil
- Implementar renovação automática de token quando expirado
- Adicionar logout do Gmail (revogar token)
- Sincronizar emails com banco de dados local

---

- [Django](https://djangoproject.com) — pelo framework sólido e bem documentado
- [Firebase](https://firebase.google.com) — pela infraestrutura de autenticação
- [shadcn/ui](https://ui.shadcn.com) — pelos componentes React acessíveis e elegantes
- [Radix UI](https://radix-ui.com) — pela base de componentes primitivos


---

## Limpeza e Otimização do Projeto

### Arquivos removidos (25/03/2026)

Para manter o projeto limpo e sem código desnecessário, foram removidos os seguintes arquivos:

#### Arquivos vazios
- `core/admin.py` - Arquivo vazio sem registros de modelos
- `core/tests.py` - Arquivo de testes vazio
- `core/models.py` - Modelo User customizado não utilizado (projeto usa `django.contrib.auth.models.User`)
- `core/database.py` - Configuração SQLAlchemy nunca importada

#### Apps vazios (não registrados em INSTALLED_APPS)
- `core/users/` - App inteiro removido (vazio e não utilizado)
  - `core/users/models.py`
  - `core/users/views.py`
  - `core/users/admin.py`
  - `core/users/tests.py`
  - `core/users/apps.py`
  - `core/users/__init__.py`
  - `core/users/migrations/__init__.py`

- `core/api/` - App inteiro removido (vazio e não utilizado)
  - `core/api/models.py`
  - `core/api/views.py`
  - `core/api/admin.py`
  - `core/api/tests.py`
  - `core/api/apps.py`
  - `core/api/__init__.py`
  - `core/api/migrations/__init__.py`

### Resultado

- ✅Conta de admin (createsuperuser):
usuário: admin
email: admin@example.com
senha: admin1234

- ✅Passo 2: acessar PF
http://127.0.0.1:8000/
login usuario / usuario1234

- ✅Passo 2: acessar PJ
http://127.0.0.1:8000/
login empresa / empresa1234