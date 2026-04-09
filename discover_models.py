#!/usr/bin/env python
"""Descobrir quais modelos Gemini estão disponíveis para sua chave"""

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexuslife.settings')
django.setup()

from django.conf import settings

try:
    import google.generativeai as genai
    
    print("🔍 Descobrindo modelos disponíveis...\n")
    
    # Configurar API
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        print("❌ GEMINI_API_KEY não configurada!")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    
    # Listar modelos
    print("📋 Modelos disponíveis para sua chave:\n")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display: {model.display_name}")
            print(f"  Descrição: {model.description}\n")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)
