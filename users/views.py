from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import CustomUser, UserProfile, Badge, Reward, UserBadge, UserReward
from django.utils import timezone


def UserAreaView(request):
    """Área principal do aventureiro - página de login ou área logada"""
    if request.user.is_authenticated:
        # Usuário logado - mostrar área interna
        try:
            # Buscar dados do usuário
            upcoming_adventures = Booking.objects.filter(
                user=request.user,
                status__in=['pending', 'approved'],
                adventure_event__date__gte=timezone.now()
            ).select_related('adventure_event__adventure').order_by('adventure_event__date')
            
            completed_adventures = Booking.objects.filter(
                user=request.user,
                status='completed'
            ).select_related('adventure_event__adventure').order_by('-adventure_event__date')
            
            # Buscar recompensas disponíveis
            available_rewards = Reward.objects.filter(
                is_active=True,
                points_cost__lte=request.user.available_points
            ).exclude(
                userreward__user=request.user,
                userreward__status__in=['pending', 'approved']
            )
        except:
            upcoming_adventures = []
            completed_adventures = []
            available_rewards = []
        
        context = {
            'upcoming_adventures': upcoming_adventures,
            'completed_adventures': completed_adventures,
            'available_rewards': available_rewards,
        }
        return render(request, 'users/area_logged.html', context)
    else:
        # Usuário não logado - mostrar página de login
        return render(request, 'users/area.html')


def UserLoginView(request):
    """Processa o login do usuário via AJAX ou POST"""
    
    # Log detalhado para debug
    print(f"\n{'='*60}")
    print(f"🔍 DEBUG LOGIN - {request.method}")
    print(f"📍 IP: {request.META.get('REMOTE_ADDR')}")
    print(f"🌐 User-Agent: {request.META.get('HTTP_USER_AGENT', 'N/A')[:100]}...")
    print(f"📨 Content-Type: {request.content_type}")
    print(f"🔒 CSRF Token (cookie): {request.COOKIES.get('csrftoken', 'N/A')[:20]}...")
    
    if request.method == 'POST':
        print(f"📝 POST Data: {dict(request.POST)}")
        print(f"🍪 Cookies: {list(request.COOKIES.keys())}")
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        
        print(f"👤 Email: {email}")
        print(f"🔑 Password length: {len(password) if password else 0}")
        print(f"💭 Remember me: {remember_me}")
        print(f"🔒 CSRF Token (form): {csrf_token[:20] if csrf_token else 'N/A'}...")
        
        if email and password:
            # Autenticar usando o email
            user = authenticate(request, username=email, password=password)
            print(f"🔐 Authentication result: {'Success' if user else 'Failed'}")
            
            if user is not None:
                login(request, user)
                print(f"✅ Login successful for user: {user.email}")
                
                # Configurar sessão se "lembrar de mim" estiver marcado
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)  # 2 semanas
                
                return redirect('users:area')
            else:
                print("❌ Authentication failed")
                messages.error(request, 'E-mail ou senha incorretos.')
        else:
            print("❌ Missing email or password")
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    print("🔄 Redirecting back to login page")
    return redirect('users:area')


def UserLogoutView(request):
    """Logout do usuário"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('users:area')


def ForgotPasswordView(request):
    """Recuperação de senha via AJAX"""
    if request.method == 'POST':
        email = request.POST.get('forgotEmail')
        
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                # Aqui você implementaria o envio de e-mail
                # Por enquanto, vamos apenas simular sucesso
                
                return JsonResponse({
                    'success': True,
                    'message': 'Instruções de recuperação enviadas para seu e-mail!'
                })
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'E-mail não encontrado em nossa base de dados.'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Por favor, informe seu e-mail.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido.'
    })


def UserRegisterView(request):
    """Registro de novo usuário"""
    if request.method == 'POST':
        try:
            # Dados básicos
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            # Validações básicas
            if not all([first_name, last_name, email, password]):
                messages.error(request, 'Todos os campos são obrigatórios.')
            elif password != password_confirm:
                messages.error(request, 'As senhas não coincidem.')
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'E-mail já cadastrado.')
            else:
                # Criar usuário
                user = CustomUser.objects.create_user(
                    email=email,
                    username=email,  # usar email como username
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('users:area')
        except Exception as e:
            messages.error(request, 'Erro ao criar conta. Tente novamente.')
    
    try:
        return render(request, 'users/register.html')
    except Exception as e:
        return HttpResponse(f"""
        <h1>📝 Cadastro</h1>
        <form method="post">
            <p><input type="text" name="first_name" placeholder="Nome" required></p>
            <p><input type="text" name="last_name" placeholder="Sobrenome" required></p>
            <p><input type="email" name="email" placeholder="E-mail" required></p>
            <p><input type="password" name="password" placeholder="Senha" required></p>
            <p><input type="password" name="password_confirm" placeholder="Confirmar Senha" required></p>
            <p><button type="submit">Cadastrar</button></p>
        </form>
        <p><a href="/area-aventureiro/">← Voltar</a></p>
        <p>Sistema funcionando - Erro: {str(e)}</p>
        """)


@login_required
def UserProfileView(request):
    """Perfil do usuário"""
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except:
        profile = None
    
    if request.method == 'POST':
        try:
            # Atualizar dados do usuário
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.phone = request.POST.get('phone', request.user.phone)
            request.user.city = request.POST.get('city', request.user.city)
            request.user.state = request.POST.get('state', request.user.state)
            request.user.experience_level = request.POST.get('experience_level', request.user.experience_level)
            request.user.save()
            
            # Atualizar perfil se existir
            if profile:
                profile.bio = request.POST.get('bio', profile.bio)
                if 'avatar' in request.FILES:
                    profile.avatar = request.FILES['avatar']
                profile.save()
            
            messages.success(request, 'Perfil atualizado com sucesso!')
        except Exception as e:
            messages.error(request, 'Erro ao atualizar perfil.')
    
    try:
        context = {
            'profile': profile,
            'badges': request.user.badges.all(),
            'total_points': request.user.total_points,
            'available_points': request.user.available_points,
        }
        return render(request, 'users/profile.html', context)
    except Exception as e:
        return HttpResponse(f'Erro ao carregar perfil: {str(e)}')


@login_required
def UserAdventuresView(request):
    """Aventuras do usuário"""
    from bookings.models import Booking
    
    try:
        bookings = Booking.objects.filter(
            user=request.user
        ).select_related(
            'event__adventure'
        ).order_by('-created_at')
        
        context = {
            'bookings': bookings,
        }
        
        return render(
            request,
            'users/adventures.html',
            context,
            content_type='text/html; charset=utf-8'
        )
        
    except Exception as e:
        # Log do erro para debug
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao carregar aventuras: {str(e)}")
        
        # Renderiza uma página de erro amigável
        return render(
            request,
            'users/adventures.html',
            {
                'bookings': [],
                'error_message': 'Desculpe, não foi possível carregar suas aventuras. Por favor, tente novamente.'
            },
            content_type='text/html; charset=utf-8'
        )


@login_required
def UserDashboardView(request):
    """Painel personalizado do cliente com todas as inscrições"""
    try:
        from bookings.models import Booking, PreRegistration
        from django.db.models import Q
        
        # Reservas do usuário
        bookings = Booking.objects.filter(user=request.user).select_related(
            'event__adventure'
        ).order_by('-created_at')
        
        # Pré-inscrições do usuário (pelo CPF)
        pre_registrations = PreRegistration.objects.filter(
            cpf=request.user.cpf
        ).select_related('event__adventure').order_by('-created_at')
        
        # Estatísticas
        total_adventures = bookings.filter(status='approved').count()
        pending_bookings = bookings.filter(status='pending').count()
        pending_pre_registrations = pre_registrations.filter(status='pending').count()
        
        # Próximas aventuras
        upcoming_bookings = bookings.filter(
            status='approved',
            event__date__gte=timezone.now().date()
        ).order_by('event__date')[:3]
        
        context = {
            'bookings': bookings,
            'pre_registrations': pre_registrations,
            'upcoming_bookings': upcoming_bookings,
            'stats': {
                'total_adventures': total_adventures,
                'pending_bookings': pending_bookings,
                'pending_pre_registrations': pending_pre_registrations,
            }
        }
        
    except Exception as e:
        print(f"Erro no dashboard: {e}")
        context = {
            'bookings': [],
            'pre_registrations': [],
            'upcoming_bookings': [],
            'stats': {
                'total_adventures': 0,
                'pending_bookings': 0,
                'pending_pre_registrations': 0,
            }
        }
    
    return render(request, 'users/dashboard.html', context)


@login_required
def RedeemRewardView(request, reward_id):
    """Resgata uma recompensa"""
    if request.method == 'POST':
        try:
            reward = get_object_or_404(Reward, id=reward_id, is_active=True)
            
            # Verificar se o usuário tem pontos suficientes
            if request.user.available_points < reward.points_cost:
                return JsonResponse({
                    'success': False,
                    'message': 'Pontos insuficientes para resgatar esta recompensa.'
                })
            
            # Verificar se o usuário já tem esta recompensa pendente/aprovada
            if UserReward.objects.filter(
                user=request.user,
                reward=reward,
                status__in=['pending', 'approved']
            ).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Você já possui esta recompensa.'
                })
            
            # Resgatar recompensa
            user_reward = request.user.redeem_reward(reward)
            if user_reward:
                return JsonResponse({
                    'success': True,
                    'message': 'Recompensa resgatada com sucesso!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro ao resgatar recompensa.'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido.'
    })


@login_required
def RequestAccountDeletionView(request):
    """Solicita exclusão da conta do usuário"""
    if request.method == 'POST':
        try:
            # Aqui você implementaria a lógica de exclusão
            # Por exemplo, marcar a conta para exclusão após 30 dias
            # ou enviar e-mail para administrador
            messages.success(
                request,
                'Solicitação de exclusão recebida. Nossa equipe entrará em contato.'
            )
            return redirect('users:area')
        except Exception as e:
            messages.error(request, f'Erro ao solicitar exclusão: {str(e)}')
            return redirect('users:profile')
    
    return redirect('users:profile') 