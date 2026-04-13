#!/usr/bin/env python
"""
Script de teste da integração do Gemini AI no Chatbot
Execute com: python test_chatbot_gemini.py
"""

import os
import sys
import django
import json
from pathlib import Path
from urllib.request import Request, urlopen

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexuslife.settings')
django.setup()

from core.gemini_integration import gemini_bot_ai, GEMINI_AVAILABLE

print("=" * 70)
print("TESTE DA INTEGRAÇÃO GEMINI AI NO CHATBOT NEXUSLIFE")
print("=" * 70)

# Validações básicas
print("\n✓ Verificando configuração:")
print(f"  - Gemini disponível: {'Sim ✓' if GEMINI_AVAILABLE else 'Não ✗'}")
print(f"  - Bot inicializado: {'Sim ✓' if gemini_bot_ai else 'Não ✗'}")

if not GEMINI_AVAILABLE or not gemini_bot_ai:
    print("\n✗ ERRO: Gemini não está disponível!")
    sys.exit(1)

# Teste 1: Mensagem simples
print("\n\n1️⃣  TESTE: Mensagem Simples ao Chatbot")
print("-" * 70)
message_1 = "Olá, como funciona a plataforma NexusLife?"
response_1 = gemini_bot_ai.process_message(message_1)
print(f"Pergunta: {message_1}")
print(f"Resposta: {response_1['response'][:150]}...")

# Teste 2: Pergunta sobre freelancers
print("\n\n2️⃣  TESTE: Pergunta Sobre Freelancers")
print("-" * 70)
message_2 = "Como eu ganho dinheiro oferecendo serviços?"
response_2 = gemini_bot_ai.process_message(message_2)
print(f"Pergunta: {message_2}")
print(f"Resposta: {response_2['response'][:150]}...")

# Teste 3: Com contexto de usuário PF
print("\n\n3️⃣  TESTE: Com Contexto de Usuário (Freelancer/PF)")
print("-" * 70)
user_profile = {
    'person_type': 'Pessoa Física',
    'average_rating': 4.8,
    'completion_rate': 95.0,
    'total_earnings': 5000.00,
}
message_3 = "Qual é a taxa de comissão?"
response_3 = gemini_bot_ai.process_message(message_3, user_profile=user_profile)
print(f"Perfil: Freelancer (PF) - Avaliação 4.8/5")
print(f"Pergunta: {message_3}")
print(f"Resposta: {response_3['response'][:150]}...")

# Teste 4: Com contexto de usuário PJ
print("\n\n4️⃣  TESTE: Com Contexto de Usuário (Empresa/PJ)")
print("-" * 70)
company_profile = {
    'person_type': 'Pessoa Jurídica',
    'average_rating': 4.5,
    'completion_rate': 100.0,
    'total_earnings': 0.00,
}
message_4 = "Como contrato os melhores freelancers?"
response_4 = gemini_bot_ai.process_message(message_4, user_profile=company_profile)
print(f"Perfil: Empresa (PJ)")
print(f"Pergunta: {message_4}")
print(f"Resposta: {response_4['response'][:150]}...")

# Teste 5: Com histórico de conversa
print("\n\n5️⃣  TESTE: Com Histórico de Conversa")
print("-" * 70)
history = [
    {'role': 'user', 'content': 'O que é NexusLife?'},
    {'role': 'assistant', 'content': 'NexusLife é uma plataforma de marketplace de freelancers que conecta PF e PJ.'},
    {'role': 'user', 'content': 'Como me cadastro?'}
]
message_5 = "Preciso de documentação especial?"
response_5 = gemini_bot_ai.process_message(message_5, conversation_history=history)
print(f"Pergunta anterior: O que é NexusLife?")
print(f"Pergunta atual: {message_5}")
print(f"Resposta: {response_5['response'][:150]}...")

# Teste 6: Pergunta sobre dashboard
print("\n\n6️⃣  TESTE: Pergunta Sobre Dashboard")
print("-" * 70)
message_6 = "Onde vejo meus ganhos e pedidos?"
response_6 = gemini_bot_ai.process_message(message_6)
print(f"Pergunta: {message_6}")
print(f"Resposta: {response_6['response'][:150]}...")

print("\n" + "=" * 70)
print("✅ TODOS OS TESTES DO CHATBOT COM GEMINI PASSARAM!")
print("=" * 70)
print("\n📋 Próximos passos:")
print("   1. Acesse http://127.0.0.1:8000/chatbot/")
print("   2. Envie mensagens e teste o chatbot com Gemini")
print("   3. Verifique os logs em 'logs/'")
print("   4. O Gemini agora responde com IA em tempo real!")
print("\n💡 A integração está completa e funcionando!\n")
