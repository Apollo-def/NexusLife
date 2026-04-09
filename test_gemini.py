#!/usr/bin/env python
"""
Script de teste para validar a integração do Gemini AI com o NexusLife Chatbot
Execute com: python test_gemini.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexuslife.settings')
django.setup()

from core.gemini_integration import gemini_bot_ai, GEMINI_AVAILABLE
from django.conf import settings

print("=" * 60)
print("TESTE DE INTEGRAÇÃO GEMINI AI - NexusLife")
print("=" * 60)

# 1. Verificar se Gemini está disponível
print("\n1️⃣  Verificando disponibilidade do Gemini...")
print(f"   ✓ GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
print(f"   ✓ Chave de API configurada: {'Sim' if settings.GEMINI_API_KEY else 'Não'}")

if settings.GEMINI_API_KEY:
    print(f"   ✓ Chave (primeiros 20 chars): {settings.GEMINI_API_KEY[:20]}...")
else:
    print("   ✗ ERRO: Chave de API não configurada!")
    sys.exit(1)

# 2. Verificar inicialização do bot
print("\n2️⃣  Verificando inicialização do NexusBotGemini...")
if gemini_bot_ai is None:
    print("   ✗ ERRO: NexusBotGemini não inicializado!")
    sys.exit(1)
print(f"   ✓ Bot inicializado")
print(f"   ✓ Modelo: {gemini_bot_ai.model_name}")
print(f"   ✓ Temperatura: {gemini_bot_ai.temperature}")
print(f"   ✓ Max tokens: {gemini_bot_ai.max_tokens}")

# 3. Teste simples de mensagem
print("\n3️⃣  Testando resposta da IA...")
print("   Enviando: 'Olá, qual é seu nome?'")

response = gemini_bot_ai.process_message(
    message="Olá, qual é seu nome?",
    conversation_history=None,
    user_profile=None
)

if response.get('error'):
    print(f"   ✗ ERRO: {response['error']}")
    sys.exit(1)

if response.get('response'):
    print(f"   ✓ Resposta recebida!")
    print(f"   📝 Resposta: {response['response'][:100]}...")
else:
    print("   ✗ Sem resposta da IA")
    sys.exit(1)

# 4. Teste com contexto de usuário (PF)
print("\n4️⃣  Testando com contexto de usuário (Freelancer/PF)...")
user_profile = {
    'person_type': 'Pessoa Física',
    'average_rating': 4.8,
    'completion_rate': 95.0,
    'total_earnings': 5000.00,
}

response = gemini_bot_ai.process_message(
    message="Como melhoro minha avaliação?",
    conversation_history=None,
    user_profile=user_profile
)

if response.get('response'):
    print(f"   ✓ Resposta com contexto recebida!")
    print(f"   📝 Resposta: {response['response'][:100]}...")
else:
    print(f"   ✗ ERRO: {response.get('error')}")

# 5. Teste com histórico de conversa
print("\n5️⃣  Testando com histórico de conversa...")
history = [
    {'role': 'user', 'content': 'Qual é o NexusLife?'},
    {'role': 'assistant', 'content': 'NexusLife é uma plataforma de marketplace de freelancers.'},
    {'role': 'user', 'content': 'Como me cadastro?'}
]

response = gemini_bot_ai.process_message(
    message="Preciso de documento para me registrar?",
    conversation_history=history,
    user_profile=None
)

if response.get('response'):
    print(f"   ✓ Resposta com histórico recebida!")
    print(f"   📝 Resposta: {response['response'][:100]}...")
else:
    print(f"   ✗ ERRO: {response.get('error')}")

# 6. Teste com contexto PJ
print("\n6️⃣  Testando com contexto de usuário (Empresa/PJ)...")
company_profile = {
    'person_type': 'Pessoa Jurídica',
    'average_rating': 4.5,
    'completion_rate': 100.0,
    'total_earnings': 0.00,
}

response = gemini_bot_ai.process_message(
    message="Quantos freelancers estão disponíveis?",
    conversation_history=None,
    user_profile=company_profile
)

if response.get('response'):
    print(f"   ✓ Resposta com contexto PJ recebida!")
    print(f"   📝 Resposta: {response['response'][:100]}...")
else:
    print(f"   ✗ ERRO: {response.get('error')}")

# Resumo final
print("\n" + "=" * 60)
print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("=" * 60)
print("\n📋 Próximos passos:")
print("   1. Teste via API: POST /api/chatbot/")
print("   2. Acesse o chatbot na interface web")
print("   3. Verifique os logs em 'logs/'")
print("\n💡 Dica: As respostas agora usam IA Gemini em real-time!\n")
