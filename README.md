<div align="center">

<img src="static/images/logo.png" alt="NexusLife Logo" width="120"/>

# NexusLife

**Plataforma web de autenticação e gerenciamento de usuários com integração Firebase**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=flat-square&logo=firebase&logoColor=black)](https://firebase.google.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

</div>

---

## Descrição

NexusLife é uma aplicação web full-stack que oferece um sistema completo de autenticação e gerenciamento de usuários. O backend é construído com Django 4.2 e integrado ao Firebase para autenticação segura, verificação de e-mail e redefinição de senha. O frontend é uma SPA moderna em React + TypeScript com componentes Radix UI e estilização via Tailwind CSS.

**Problema que resolve:** Projetos que precisam de um ponto de partida sólido para autenticação de usuários, com dupla camada de segurança (Django Auth + Firebase Auth), sem precisar construir do zero.

**Público-alvo:** Desenvolvedores que precisam de um boilerplate robusto de autenticação com Django e Firebase, ou equipes que querem uma base para construir aplicações SaaS.

**Diferenciais:**
- Autenticação dupla: Django Auth (sessão) + Firebase Auth (JWT)
- Verificação de e-mail automática via Firebase no cadastro
- Redefinição de senha via Firebase sem configuração de SMTP
- Dados de perfil sincronizados no Firestore
- Frontend desacoplado com React + Vite + shadcn/ui
- Degradação graciosa: o servidor funciona mesmo sem as credenciais do Firebase

---

## Demonstração

### Fluxo de autenticação

```
[Cadastro] → Cria usuário no Django + Firebase Auth + Firestore
           → Envia e-mail de verificação automaticamente

[Login]    → Autentica via Django (suporta username, e-mail ou CPF)
           → Redireciona para /home (rota protegida)

[Perfil]   → Atualiza nome, sobrenome e e-mail
           → Protegido por @login_required

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
| Railway | ✅ | — |
| Render | ✅ | ✅ |
| Heroku | ✅ | — |
| Vercel | — | ✅ |
| Netlify | — | ✅ |
| VPS (Ubuntu + Nginx) | ✅ | ✅ |

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

## Agradecimentos

- [Django](https://djangoproject.com) — pelo framework sólido e bem documentado
- [Firebase](https://firebase.google.com) — pela infraestrutura de autenticação
- [shadcn/ui](https://ui.shadcn.com) — pelos componentes React acessíveis e elegantes
- [Radix UI](https://radix-ui.com) — pela base de componentes primitivos
