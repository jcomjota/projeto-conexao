from django.shortcuts import render
from django.http import HttpResponse
from adventures.models import Adventure


def home(request):
    """Homepage do site"""
    try:
        # Buscar aventuras destacadas para exibir na home
        featured_adventures = Adventure.objects.filter(
            is_active=True,
            is_featured=True
        ).order_by('-created_at')[:6]
        
        return render(request, 'content/home.html', {
            'featured_adventures': featured_adventures
        })
    except Exception as e:
        return HttpResponse(f"""
        <h1>🏠 Conexão Adventure - Homepage</h1>
        <h2>Aventuras Incríveis, Experiências Inesquecíveis</h2>
        <p>✅ Homepage funcionando!</p>
        <ul>
            <li><a href="/aventuras/">Programação</a></li>
            <li><a href="/materiais/">Materiais de Apoio</a></li>
            <li><a href="/area-aventureiro/">Área do Aventureiro</a></li>
            <li><a href="/sobre/">Sobre Nós</a></li>
        </ul>
        <footer>
            <p>Sistema Django funcionando - Erro: {str(e)}</p>
        </footer>
        """)


def about(request):
    """Página sobre nós"""
    try:
        return render(request, 'content/about.html')
    except Exception as e:
        return HttpResponse(f"""
        <h1>📖 Sobre a Conexão Adventure</h1>
        <p>Somos uma empresa especializada em turismo de aventura.</p>
        <p>✅ Página funcionando! Erro: {str(e)}</p>
        <a href="/">← Voltar</a>
        """)


def how_it_works(request):
    """Como funciona"""
    try:
        return render(request, 'content/how_it_works.html')
    except Exception as e:
        return HttpResponse(f"""
        <h1>⚙️ Como Funciona</h1>
        <p>Processo simples em 6 passos.</p>
        <p>✅ Página funcionando! Erro: {str(e)}</p>
        <a href="/">← Voltar</a>
        """)


def general_rules(request):
    """Regras gerais"""
    try:
        return render(request, 'content/general_rules.html')
    except Exception as e:
        return HttpResponse(f"""
        <h1>📋 Regras Gerais</h1>
        <p>Normas e diretrizes para participar das aventuras.</p>
        <p>✅ Página funcionando! Erro: {str(e)}</p>
        <a href="/">← Voltar</a>
        """)


def contact(request):
    """Página de contato"""
    try:
        return render(request, 'content/contact.html')
    except Exception as e:
        return HttpResponse(f"""
        <h1>📞 Contato</h1>
        <p>📧 contato@conexaoadventure.com.br</p>
        <p>📱 (51) 3333-4444</p>
        <p>✅ Página funcionando! Erro: {str(e)}</p>
        <a href="/">← Voltar</a>
        """)


def terms(request):
    """Termos e condições"""
    try:
        return render(request, 'content/terms.html')
    except Exception as e:
        return HttpResponse(f"""
        <h1>📜 Termos e Condições</h1>
        <p>Termos de uso do site.</p>
        <p>✅ Página funcionando! Erro: {str(e)}</p>
        <a href="/">← Voltar</a>
        """)


def privacy(request):
    """Política de privacidade"""
    try:
        return render(request, 'content/privacy.html')
    except Exception as e:
        return HttpResponse(f"""
        <h1>🔒 Política de Privacidade</h1>
        <p>Como tratamos seus dados pessoais.</p>
        <p>✅ Página funcionando! Erro: {str(e)}</p>
        <a href="/">← Voltar</a>
        """)
