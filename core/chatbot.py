import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

# Configurações do chatbot
CHATBOT_CONFIG = {
    'name': 'NexusBot',
    'version': '1.0',
    'responses': {
        'oi': ['Olá! Sou o NexusBot, assistente do NexusLife! Como posso ajudar você hoje?', 'Oi! Bem-vindo ao NexusLife! O que você precisa?'],
        'ola': ['Olá! Sou o NexusBot, assistente do NexusLife! Como posso ajudar você hoje?', 'Oi! Bem-vindo ao NexusLife! O que você precisa?'],
        'bom dia': ['Bom dia! <i class="fas fa-sun"></i> Como posso ajudar você no NexusLife hoje?', 'Bom dia! O NexusLife está aqui para ajudar!'],
        'boa tarde': ['Boa tarde! <i class="fas fa-cloud-sun"></i> Como posso auxiliar você na nossa plataforma?', 'Boa tarde! Pronto para ajudar com o NexusLife!'],
        'boa noite': ['Boa noite! <i class="fas fa-moon"></i> Como posso ajudar você agora?', 'Boa noite! O NexusLife nunca dorme para ajudar você!'],
        'ajuda': ['Estou aqui para ajudar! Você pode perguntar sobre:\n• Como se cadastrar (PF/PJ)\n• Como contratar serviços\n• Como oferecer serviços\n• Como usar o marketplace\n• Problemas com conta\n• Sistema de avaliações\n• Dashboards PF/PJ'],
        'cadastro': ['Para se cadastrar no NexusLife:\n1. Clique em "Registrar" no menu\n2. Escolha PF (Pessoa Física) ou PJ (Pessoa Jurídica)\n3. Preencha seus dados pessoais\n4. Para PJ: inclua inscrição estadual\n5. Verifique seu e-mail\n6. Complete seu perfil no dashboard'],
        'pf': ['Pessoa Física no NexusLife:\n• Perfil para freelancers individuais\n• Ofereça serviços como designer, programador, etc.\n• Dashboard simplificado em /marketplace/dashboard/pf/\n• Gerencie seus serviços e pedidos\n• Receba avaliações dos clientes'],
        'pj': ['Pessoa Jurídica no NexusLife:\n• Perfil para empresas/agências\n• Contrate freelancers para projetos\n• Dashboard completo em /marketplace/dashboard/pj/\n• Gerencie múltiplos pedidos\n• Avalie freelancers contratados'],
        'servicos': ['Para contratar serviços no NexusLife:\n1. Faça login como PJ\n2. Vá para "Marketplace" no menu\n3. Navegue pelos serviços disponíveis\n4. Use filtros por categoria/preço\n5. Clique em "Contratar" no serviço desejado\n6. Preencha detalhes do pedido\n7. Acompanhe no seu dashboard'],
        'freelancer': ['Para oferecer serviços como freelancer:\n1. Cadastre-se como PF (Pessoa Física)\n2. Complete seu perfil em /profile/\n3. Adicione suas habilidades e experiência\n4. Crie serviços em /marketplace/service/create/\n5. Defina preços e descrições\n6. Receba pedidos no dashboard\n7. Entregue trabalhos e receba avaliações'],
        'marketplace': ['O Marketplace NexusLife oferece:\n• Serviços digitais diversos\n• Filtros por categoria e preço\n• Perfis de freelancers verificados\n• Sistema de avaliações\n• Pedidos seguros\n• Dashboards separados PF/PJ\n• Favoritos para salvar serviços'],
        'dashboard': ['Dashboards NexusLife:\n\nPara PF (Freelancer):\n• /marketplace/dashboard/pf/\n• Meus serviços oferecidos\n• Pedidos recebidos\n• Avaliações recebidas\n\nPara PJ (Cliente):\n• /marketplace/dashboard/pj/\n• Serviços contratados\n• Pedidos em andamento\n• Histórico de compras'],
        'avaliacao': ['Sistema de avaliações NexusLife:\n• Clientes avaliam freelancers (1-5 estrelas)\n• Comentários sobre qualidade do trabalho\n• Avaliações aparecem nos perfis\n• Média calculada automaticamente\n• Ajuda outros usuários na escolha\n• Freelancers podem responder comentários'],
        'favoritos': ['Sistema de Favoritos:\n• Salve serviços que interessam\n• Acesse rapidamente depois\n• Compare preços e avaliações\n• Organize seus interesses\n• Receba notificações (futuro)\n• Lista pessoal no seu perfil'],
        'pedido': ['Como funciona um pedido:\n1. Cliente contrata serviço\n2. Freelancer recebe notificação\n3. Combinam detalhes e prazo\n4. Freelancer executa trabalho\n5. Entrega final\n6. Cliente aprova e paga\n7. Avaliação é feita\n8. Reputação aumenta'],
        'problema': ['Problemas comuns e soluções:\n\nLogin/Registro:\n• Verifique email e senha\n• Use "Esqueci senha" se necessário\n• Limpe cache do navegador\n\nPedidos:\n• Verifique status no dashboard\n• Contate freelancer diretamente\n• Use suporte se necessário\n\nPerfil:\n• Complete todas informações\n• Adicione foto profissional\n• Verifique dados PF/PJ'],
        'contato': ['Para suporte no NexusLife:\n• Use este chatbot 24/7\n• Acesse "Ajuda" no seu dashboard\n• Consulte a documentação em README.md\n• Para questões urgentes: verifique seu painel de controle\n• Relate problemas através do sistema de suporte integrado'],
        'preco': ['Precificação no NexusLife:\n\nPara Freelancers (PF):\n• Defina seus próprios preços\n• Crie pacotes (básico/premium)\n• Negocie diretamente com clientes\n\nPara Clientes (PJ):\n• Compare preços de diferentes freelancers\n• Pacotes ajudam a escolher o ideal\n• Pagamento seguro garantido\n• Sem taxas ocultas na contratação'],
        'seguranca': ['Segurança no NexusLife:\n• Plataforma segura para freelancers e clientes\n• Pagamentos protegidos\n• Verificação de perfis de usuários\n• Sistema de avaliações para confiança\n• Suporte para resolução de disputas\n• Dados pessoais criptografados\n• Ambiente confiável para negócios digitais'],
        'default': ['Desculpe, não entendi sua pergunta sobre o NexusLife. Tente:\n• "ajuda" - ver todas opções\n• "cadastro" - como se registrar\n• "servicos" - contratar freelancers\n• "freelancer" - oferecer serviços\n• "dashboard" - gerenciar conta\n• Ou reformule sua pergunta!']
    }
}

def get_chatbot_response(message):
    """Processa a mensagem e retorna uma resposta apropriada"""
    if not message:
        return "Por favor, digite uma mensagem."

    message = message.lower().strip()

    # Verificar correspondências exatas
    for key, responses in CHATBOT_CONFIG['responses'].items():
        if key in message:
            return responses[0] if isinstance(responses, list) else responses

    # Verificar palavras-chave parciais
    keywords = {
        'cadastro': 'cadastro',
        'registrar': 'cadastro',
        'conta': 'cadastro',
        'login': 'cadastro',
        'cadastrar': 'cadastro',
        'pf': 'pf',
        'pessoa fisica': 'pf',
        'freelancer': 'freelancer',
        'trabalhar': 'freelancer',
        'oferecer': 'freelancer',
        'pj': 'pj',
        'pessoa juridica': 'pj',
        'empresa': 'pj',
        'cliente': 'pj',
        'contratar': 'servicos',
        'servico': 'servicos',
        'serviços': 'servicos',
        'contratar': 'servicos',
        'marketplace': 'marketplace',
        'plataforma': 'marketplace',
        'dashboard': 'dashboard',
        'painel': 'dashboard',
        'avaliacao': 'avaliacao',
        'avaliação': 'avaliacao',
        'avaliações': 'avaliacao',
        'avaliacoes': 'avaliacao',
        'review': 'avaliacao',
        'estrelas': 'avaliacao',
        'favoritos': 'favoritos',
        'favorito': 'favoritos',
        'salvar': 'favoritos',
        'pedido': 'pedido',
        'ordem': 'pedido',
        'projeto': 'pedido',
        'problema': 'problema',
        'erro': 'problema',
        'nao funciona': 'problema',
        'bug': 'problema',
        'contato': 'contato',
        'suporte': 'contato',
        'ajuda': 'contato',
        'preco': 'preco',
        'preço': 'preco',
        'preços': 'preco',
        'precos': 'preco',
        'custa': 'preco',
        'valor': 'preco',
        'custo': 'preco',
        'seguranca': 'seguranca',
        'segurança': 'seguranca',
        'seguro': 'seguranca',
        'protegido': 'seguranca'
    }

    for keyword, response_key in keywords.items():
        if keyword in message:
            responses = CHATBOT_CONFIG['responses'][response_key]
            return responses[0] if isinstance(responses, list) else responses

    # Resposta padrão
    return CHATBOT_CONFIG['responses']['default'][0]

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_view(request):
    """View para processar mensagens do chatbot"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'Mensagem vazia'}, status=400)

        response = get_chatbot_response(user_message)

        return JsonResponse({
            'response': response,
            'bot_name': CHATBOT_CONFIG['name'],
            'timestamp': str(request.META.get('HTTP_DATE', ''))
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        logger.error(f"Erro no chatbot: {e}")
        return JsonResponse({'error': 'Erro interno do servidor'}, status=500)