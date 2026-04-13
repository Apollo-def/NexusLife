# 🚀 Painel Administrativo NexusLife - Guia Completo

## Acesso ao Admin

**URL:** http://127.0.0.1:8000/admin/

**Login padrão (se criado):**
- Username: `admin`
- Senha: A senha que você definiu ao criar o superuser

### Comando para criar um superuser (se não tiver um):
```bash
python manage.py createsuperuser
```

---

## 📊 Módulos de Administração

### 1. **👤 Usuários** (`/admin/auth/user/`)
Gerencie todos os usuários da plataforma com interface profissional:
- **Lista de Usuários:** Visualize todos os usuários com badges coloridas
  - 👑 Superadmin (vermelho)
  - 👨‍💼 Staff (amarelo)
  - 👤 Usuário Regular (verde)
- **Filtros:** Por status (ativo/inativo), tipo de usuário, data de cadastro
- **Busca:** Por username, email, nome, sobrenome
- **Ações:** Ativar/desativar usuários, alterar permissões
- **Detalhes:** Informações completas incluindo data de cadastro e último acesso

### 2. **📋 Perfis de Usuário** (`/admin/core/userprofile/`)
Gerenciador de tipos de usuário (PF/PJ) e dados adicionais:
- **Tipo de Pessoa:** 👤 Freelancer (PF) ou 🏢 Empresa (PJ)
- **Validação:** CPF/CNPJ, Telefone
- **Status Visual:** Ativo/Inativo com cores
- **Busca:** Por username, email, CPF/CNPJ
- **Histórico:** Datas de criação e atualização

### 3. **📨 Notificações** (`/admin/core/notification/`)
Sistema de notificações para usuários:
- **Tipos:** 📦 Pedidos, ⭐ Avaliações, 💬 Mensagens, ⚙️ Sistema
- **Status:** Lida/Não Lida com indicadores visuais
- **Filtros:** Por tipo, status de leitura, data
- **Detalhes:** Visualize mensagens completas formatadas
- **Ações:** Marcar como lido/não lido em massa

### 4. **💬 Chatbot** (`/admin/core/chatbotconversation/`)
Gerenciar conversas com o Gemini AI:
- **Conversas:** Visualize sessões com Gemini
- **Usuários:** Links diretos para os perfis de usuário
- **Status:** Conversas ativas/fechadas
- **Mensagens:** Contagem e preview de mensagens
- **Histórico:** Datas completas de criação e atualização
- **Inline Messages:** Veja todas as mensagens de uma conversa sem sair da página

### 5. **📝 Serviços** (`/admin/marketplace/service/`)
Catálogo de serviços disponíveis:
- **Informações:** Título, descrição, freelancer, categoria
- **Preço:** Exibido em verde para fácil visualização
- **Avaliações:** ⭐ Nota com estrelas (1-5)
- **Status:** Serviço ativo/inativo com badges
- **Estatísticas:** Total de pedidos e avaliações
- **Filtros:** Por categoria, status, data de criação
- **Busca Avançada:** Por título, descrição, freelancer

### 6. **📦 Pedidos** (`/admin/marketplace/order/`)
Gerenciar pedidos e transações:
- **Status:** 🔧 Pendente, ⏱️ Em progresso, ✅ Concluído, ❌ Cancelado
- **Valores:** Exibidos em verde com formatação de moeda
- **Timeline:** Datas de criação, atualização e conclusão
- **Filtros:** Por status, data, usuário
- **Links:** Acesso rápido ao serviço e cliente
- **Ações:** Alterar status, atualizar valores

### 7. **⭐ Avaliações** (`/admin/marketplace/review/`)
Sistema de reviews e comentários:
- **Notas:** De 1 a 5 estrelas com exibição visual
- **Comentários:** Com preview truncado (primeiras 40 caracteres)
- **Filtros:** Por nota, data
- **Busca:** Por serviço, avaliador, comentário
- **Histórico:** Data de criação e atualização
- **Links:** Acesso direto ao avaliador e serviço

### 8. **❤️ Favoritos** (`/admin/marketplace/favorite/`)
Controle de serviços favoritados:
- **Badge:** ❤️ com ID em vermelho
- **Links:** Rápido acesso ao usuário e serviço
- **Timeline:** Data de adição aos favoritos
- **Filtros:** Por data
- **Busca:** Por usuário ou serviço

### 9. **👨‍💻 Perfis de Freelancer** (`/admin/marketplace/freelancerprofile/`)
Gerenciar perfis profissionais de freelancers:
- **Avaliação:** ⭐ Com estrelas e nota de 1-5
- **Estatísticas:**
  - 💬 Total de avaliações
  - 📊 Taxa de conclusão (com barra de progresso colorida)
  - 💰 Ganhos totais
  - ✅ Status de verificação
- **Filtros:** Por verificação, data
- **Busca:** Por username, email, bio
- **Informações:** Bio, avaliações, taxa de conclusão, ganhos

### 10. **📂 Categorias** (`/admin/marketplace/category/`)
Categorias de serviços:
- **Emojis:** Cada categoria tem um emoji apropriado
- **Contagem:** Total de serviços por categoria
- **Data:** Data de criação
- **Simples:** Interface limpa para gerenciamento rápido

---

## 🎨 Recursos Visuais

### Badges e Cores
- **Verde (#28a745):** Ativo, Sucesso, Verificado
- **Azul (#007bff):** Informação, Padrão, Primário
- **Vermelho (#dc3545):** Crítico, Deletar, Inativo
- **Amarelo (#ffc107):** Aviso, Pendente
- **Cinza (#6c757d):** Secundário, Desativ

### Emojis para Fácil Identificação
- 👤 Usuário/Freelancer
- 🏢 Empresa
- 📝 Serviço/Conteúdo
- 💰 Preço/Valor/Transação
- ⭐ Avaliação
- 📦 Pedido
- 💬 Conversa/Mensagem
- ❤️ Favorito
- ✅ Verificado/Ativo
- 🔐 Segurança/Permissões
- 📊 Estatísticas

---

## ⚙️ Funcionalidades Avançadas

### 1. **Filtros Inteligentes**
- Filtros por data com hierarquia (date_hierarchy)
- Filtros por tipo/categoria/status
- Filtros por relacionamentos

### 2. **Busca Avançada**
- Busca em múltiplos campos
- Suporta busca por email, username, IDs
- Busca em campos relacionados (usuários, serviços)

### 3. **Dados Somente Leitura**
- Campos de timestamp protegidos
- IDs não podem ser alterados
- Histórico de modificações preservado

### 4. **Collapse (Recolhível)**
- Seções expandíveis para informações extras
- Mantém interface limpa
- Acesso rápido a dados importantes

### 5. **Inline Editing**
- Editar mensagens de chatbot na própria página de conversa
- Visualizar relacionamentos sem sair da página
- Adicionar/remover instâncias relacionadas

---

## 💡 Dicas de Uso

### Navegação Rápida
1. Use a barra de pesquisa para encontrar usuários/serviços rapidamente
2. Os links em azul levam a registros relacionados
3. Use as seções collapse para acessar dados avançados

### Gerenciamento em Massa
- Selecione múltiplos registros
- Use ações em massa para operações rápidas
- Exemplo: Bloquear múltiplos usuários de uma vez

### Organização de Dados
- Os registros mais recentes aparecem primeiro (por padrão)
- Use date_hierarchy para navegar por datas
- Filtre por status para encontrar casos urgentes

### Monitoramento
- Dashboard mostra resumo de todas as funcionalidades
- Veja estatísticas de usuários, serviços e pedidos
- Acompanhe conversas da IA em tempo real

---

## 🔒 Segurança

- Apenas usuários autenticados podem acessar o admin
- Permissões granulares (ler, criar, editar, deletar)
- Diferenciação de permissões por grupo
- Log de alterações por usuário e timestamp

---

## 📱 Responsividade

O painel de admin é totalmente responsivo:
- ✓ Otimizado para desktop
- ✓ Adaptado para tablets
- ✓ Suporta mobile (com algumas limitações de espaço)

---

## 🚀 Primeiro Login

1. Acesse http://127.0.0.1:8000/admin/
2. Faça login com suas credenciais de superuser
3. Você será redirecionado para o dashboard principal
4. Clique em qualquer módulo para começar a gerenciar
5. Use a barra de pesquisa para encontrar registros

---

## Customizações Futuras

Este painel pode ser expandido com:
- Dashboard com gráficos
- Relatórios em PDF
- Exportação de dados (CSV, Excel)
- Actions customizadas
- Filtros avançados com data range
- Integração com serviços externos
- Notificações em tempo real

---

**Desenvolvido com ❤️ para NexusLife**
