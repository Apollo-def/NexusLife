# 🤖 Ativação do Chatbot AI - NexusLife

## Como Ativar o Chatbot AI após Instalar as Dependências

O NexusLife inclui um **Chatbot AI inteligente** que usa Google Gemini ou OpenAI. Após instalar as dependências do projeto, você pode ativar o Chatbot AI seguindo os passos abaixo.

---

## 1. Verificar Dependências Instaladas

As dependências de IA já estão incluídas em `requirements.txt`:
- `google-generativeai` (para Gemini AI)
- `openai` (para OpenAI)

Confirme a instalação:
```bash
pip install -r requirements.txt
```

---

## 2. Obter Chaves de API

### Opção A: Google Gemini AI (Recomendado)

1. Acesse: https://ai.google.dev/
2. Clique em "Get API Key"
3. Crie uma chave de API gratuita
4. Copie a chave (começa com `AIzaSy...`)

### Opção B: OpenAI

1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova chave de API
3. Copie a chave (começa com `sk-...`)

---

## 3. Configurar Chave no Arquivo .env

1. Abra o arquivo `.env` na raiz do projeto
2. Adicione a chave de API:

**Para Gemini:**
```env
GEMINI_API_KEY=AIzaSy...aqui-sua-chave...
```

**Para OpenAI:**
```env
OPENAI_API_KEY=sk-...aqui-sua-chave...
```

---

## 4. Ativar o Chatbot AI

Execute o comando de ativação:

```bash
python manage.py activate_chatbot_ai
```

**Resultado Esperado:**
```
[BOT] Ativando Chatbot AI...

[INFO] Verificando Google Generative AI (Gemini)...
  [OK] google-generativeai instalado
  [OK] GEMINI_API_KEY configurada
  [OK] Gemini AI inicializado com sucesso!

[RELATORIO] ATIVACAO DE CHATBOT AI
============================================================

[SUCESSO] Chatbot AI ATIVADO com sucesso!

  [+] Usando: Google Generative AI (Gemini)

[ENDPOINTS] Disponíveis:
  * POST /api/chatbot/ - Enviar mensagem ao chatbot
  * GET /chatbot/ - Página do chatbot

[PRONTO] Chatbot pronto para usar!
```

---

## 5. Testar o Chatbot AI

### Opção A: Interface Web
1. Acesse: http://localhost:8000/chatbot/
2. Digite uma mensagem
3. O chatbot responderá com IA!

### Opção B: API REST
```bash
curl -X POST http://localhost:8000/api/chatbot/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Oi, como funciona o marketplace?"}'
```

**Resposta Esperada:**
```json
{
  "session_id": "uuid-aqui",
  "message": "Ola! Sou o NexusBot, um assistente inteligente...",
  "ai_enabled": true,
  "ai_provider": "Gemini"
}
```

---

## 6. Troubleshooting

### Problema: "GEMINI_API_KEY não configurada"

**Solução:**
- Verifique se o arquivo `.env` existe
- Confirme que a chave está no formato correto
- Reinicie o servidor Django: `python manage.py runserver`

### Problema: "google-generativeai não instalado"

**Solução:**
```bash
pip install google-generativeai
python manage.py activate_chatbot_ai
```

### Problema: "Chatbot AI não disponível"

**Solução:**
- Instale `google-generativeai` ou `openai`
- Configure uma chave de API válida no `.env`
- Execute `python manage.py activate_chatbot_ai` novamente

### Problema: UnicodeEncodeError no Windows

**Solução:**
- Use PowerShell em vez do CMD
- Ou adicione isto ao início do `manage.py`:
```python
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
```

---

## 7. Logs e Monitoramento

Verifique os logs de ativação do Chatbot AI:

```bash
# Ver logs do Django em tempo real
python manage.py runserver

# Buscar por logs de IA
grep -i "chatbot AI" logs/debug.log
```

---

## 8. Recursos

- **Documentação Gemini:** https://ai.google.dev/gemini-api/docs
- **Documentação OpenAI:** https://platform.openai.com/docs
- **Código do Chatbot:** `core/chatbot_enhanced.py`
- **Integração Gemini:** `core/gemini_integration.py`
- **Integração OpenAI:** `core/openai_integration.py`

---

## 9. Próximos Passos

Após ativar o Chatbot AI:

1. ✅ Teste no `/chatbot/` ou `/api/chatbot/`
2. 📊 Monitore conversas em `Admin Panel > Chatbot Conversations`
3. 🔧 Customize o prompt do chatbot em `core/gemini_integration.py`
4. 🚀 Deploy em produção com variáveis de ambiente seguras

---

**Pronto! Seu Chatbot AI está funcionando!** 🎉

Se tiver dúvidas, consulte o README.md ou a documentação do projeto.
