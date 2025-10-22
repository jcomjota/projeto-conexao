document.addEventListener('DOMContentLoaded', function() {
    // Menu Mobile - Sistema de Overlay em Tela Cheia
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const menu = document.querySelector('.menu');
    const body = document.body;
    
    // Criar botão de fechar se não existir
    let closeBtn = document.querySelector('.menu-close-btn');
    if (!closeBtn && menu) {
        closeBtn = document.createElement('button');
        closeBtn.className = 'menu-close-btn';
        closeBtn.innerHTML = '&times;';
        closeBtn.setAttribute('aria-label', 'Fechar menu');
        menu.appendChild(closeBtn);
    }
    
    // Função para abrir o menu
    function openMenu() {
        if (menu) {
            menu.classList.add('active');
            body.classList.add('menu-open');
        }
        // Ocultar botão hamburguer
        if (mobileMenuBtn) {
            mobileMenuBtn.classList.add('hidden');
        }
    }
    
    // Função para fechar o menu
    function closeMenu() {
        if (menu) {
            menu.classList.remove('active');
            body.classList.remove('menu-open');
        }
        
        // Mostrar botão hamburguer novamente
        if (mobileMenuBtn) {
            mobileMenuBtn.classList.remove('hidden');
        }
        
        // Fechar todos os dropdowns
        const dropdowns = document.querySelectorAll('.dropdown');
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    }
    
    // Event listener para o botão hamburguer
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (menu && menu.classList.contains('active')) {
                closeMenu();
            } else {
                openMenu();
            }
        });
    }
    
    // Event listener para o botão de fechar (X)
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            closeMenu();
        });
    }
    
    // Fechar menu ao clicar em um link (exceto dropdowns)
    const menuLinks = menu ? menu.querySelectorAll('a:not(.dropdown > a)') : [];
    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            closeMenu();
        });
    });
    
    // Fechar menu com tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && menu && menu.classList.contains('active')) {
            closeMenu();
        }
    });
    
    // Dropdown functionality para mobile
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
        
        if (link) {
            link.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    dropdown.classList.toggle('active');
                    
                    // Fechar outros dropdowns
                    dropdowns.forEach(otherDropdown => {
                        if (otherDropdown !== dropdown && otherDropdown.classList.contains('active')) {
                            otherDropdown.classList.remove('active');
                        }
                    });
                }
            });
        }
    });
    
    // Fechar menu ao redimensionar a tela para desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && menu && menu.classList.contains('active')) {
            closeMenu();
        }
    });
    
    // Formulário de Newsletter
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            if (email) {
                // Aqui você adicionaria a lógica para enviar o email para seu servidor
                alert('Obrigado por se inscrever! Em breve você receberá nossas novidades.');
                this.reset();
            }
        });
    }
    
    // Adicionar efeito de scroll suave para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Ignorar se for um link de dropdown ou # simples
            if (href === '#' || this.parentElement.classList.contains('dropdown')) {
                return;
            }
            
            e.preventDefault();
            
            const targetElement = document.querySelector(href);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
                
                // Fechar o menu móvel se estiver aberto
                if (menu.classList.contains('active')) {
                    menu.classList.remove('active');
                    const icon = mobileMenuBtn.querySelector('i');
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    });
    
    // Animar as partículas no hero
    animateParticles();
    
    // Animar elementos ao scroll
    animateOnScroll();
    
    // Adicionar números de contagem aos stats na hero section
    animateCounters();
    
    // Inicializar o slideshow
    initSlideshow();
    
    // Adicionar evento de redimensionamento para ajustar o hero
    window.addEventListener('resize', adjustHeroHeight);
    
    // Ajustar altura do hero inicialmente
    adjustHeroHeight();
    
    // Inicializar funcionalidades específicas da página de downloads
    initDownloadsPage();

    // === LOGIN FUNCTIONALITY === 

    // Toggle password visibility
    function togglePassword() {
        const passwordInput = document.getElementById('password');
        const toggleIcon = document.getElementById('toggleIcon');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        }
    }

    // Show forgot password modal
    function showForgotPassword() {
        const modal = document.getElementById('forgotPasswordModal');
        if (modal) {
            modal.style.display = 'block';
        }
    }

    // Close forgot password modal
    function closeForgotPassword() {
        const modal = document.getElementById('forgotPasswordModal');
        if (modal) {
            modal.style.display = 'none';
            
            // Reset form
            const form = document.getElementById('forgotPasswordForm');
            if (form) {
                form.reset();
            }
        }
    }

    // Show login notification
    function showLoginNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotification = document.querySelector('.login-notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // Create notification
        const notification = document.createElement('div');
        notification.className = `login-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            padding: 15px 20px;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transform: translateX(100%);
            transition: transform 0.3s ease-out;
            max-width: 400px;
            background: ${type === 'success' ? 'var(--secondary-color)' : type === 'error' ? '#dc3545' : 'var(--primary-color)'};
        `;
        
        const content = notification.querySelector('.notification-content');
        content.style.cssText = `
            display: flex;
            align-items: center;
            gap: 10px;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }

    // Initialize login page functionality
    function initLoginPage() {
        // Login form submission
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                // Mostrar estado de loading
                const submitBtn = this.querySelector('.btn-login');
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Entrando...';
                    submitBtn.disabled = true;
                }
            });
        }
        
        // Forgot password form submission
        const forgotPasswordForm = document.getElementById('forgotPasswordForm');
        if (forgotPasswordForm) {
            forgotPasswordForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const email = document.getElementById('forgotEmail').value;
                
                if (email) {
                    // Show loading state
                    const submitBtn = this.querySelector('.btn-primary');
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
                    submitBtn.disabled = true;
                    
                    // Send request to backend
                    fetch('/area-aventureiro/forgot-password/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        body: JSON.stringify({ email: email })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showLoginNotification('Instruções de recuperação enviadas para seu e-mail!', 'success');
                            closeForgotPassword();
                        } else {
                            showLoginNotification(data.message || 'Erro ao enviar instruções. Tente novamente.', 'error');
                        }
                    })
                    .catch(error => {
                        showLoginNotification('Erro ao enviar instruções. Tente novamente.', 'error');
                    })
                    .finally(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    });
                } else {
                    showLoginNotification('Por favor, digite seu e-mail.', 'error');
                }
            });
        }
        
        // Close modal when clicking outside
        const modal = document.getElementById('forgotPasswordModal');
        if (modal) {
            window.onclick = function(event) {
                if (event.target == modal) {
                    closeForgotPassword();
                }
            }
        }
        
        // Close modal with ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeForgotPassword();
            }
        });
    }

    // Initialize login functionality when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Check if we're on the login page
        if (document.querySelector('.login-section')) {
            initLoginPage();
        }
    });
});

// Função para animar as partículas
function animateParticles() {
    const particles = document.querySelectorAll('.particle');
    
    if (particles.length > 0) {
        particles.forEach(particle => {
            // Posição aleatória inicial
            const randomX = Math.random() * 80 + 10; // Entre 10% e 90%
            const randomY = Math.random() * 80 + 10; // Entre 10% e 90%
            
            particle.style.left = `${randomX}%`;
            particle.style.top = `${randomY}%`;
            
            // Tamanho aleatório
            const size = Math.random() * 60 + 20; // Entre 20px e 80px
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            // Opacidade aleatória
            const opacity = Math.random() * 0.2 + 0.1; // Entre 0.1 e 0.3
            particle.style.backgroundColor = `rgba(255, 255, 255, ${opacity})`;
            
            // Atraso de animação aleatório
            const delay = Math.random() * 5; // Entre 0 e 5 segundos
            particle.style.animationDelay = `${delay}s`;
        });
    }
}

// Função para animar elementos ao scroll
function animateOnScroll() {
    const animatedElements = document.querySelectorAll('.photo-item, .testimonial-item, .value-item, .adventure-item');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
        // Adicionar classe para animação inicial (CSS)
        element.classList.add('will-animate');
    });
}

// Função para animar contadores
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    if (counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const value = target.textContent;
                    
                    // Remover caracteres não numéricos para obter o valor
                    const numValue = parseInt(value.replace(/\D/g, ''));
                    
                    // Caracteres não numéricos
                    const suffix = value.replace(/[0-9]/g, '');
                    
                    // Contador de 0 até o valor final
                    let count = 0;
                    const duration = 2000; // 2 segundos
                    const interval = Math.floor(duration / numValue);
                    
                    // Iniciar em 0
                    target.textContent = "0" + suffix;
                    
                    const timer = setInterval(() => {
                        count++;
                        target.textContent = count + suffix;
                        
                        if (count >= numValue) {
                            clearInterval(timer);
                        }
                    }, interval);
                    
                    observer.unobserve(target);
                }
            });
        }, {
            threshold: 0.5
        });
        
        counters.forEach(counter => {
            observer.observe(counter);
        });
    }
}

// Função para inicializar o slideshow
function initSlideshow() {
    const slides = document.querySelectorAll('.slide');
    const indicators = document.querySelectorAll('.indicator');
    const prevBtn = document.querySelector('.prev-slide');
    const nextBtn = document.querySelector('.next-slide');
    
    if (slides.length === 0) return;
    
    let currentIndex = 0;
    let slideInterval;
    
    // Iniciar o slideshow automático
    startSlideshow();
    
    // Funções de controle do slideshow
    function startSlideshow() {
        slideInterval = setInterval(nextSlide, 5000); // Muda a cada 5 segundos
    }
    
    function stopSlideshow() {
        clearInterval(slideInterval);
    }
    
    function nextSlide() {
        goToSlide((currentIndex + 1) % slides.length);
    }
    
    function prevSlide() {
        goToSlide((currentIndex - 1 + slides.length) % slides.length);
    }
    
    function goToSlide(index) {
        // Remover classe active do slide atual
        slides[currentIndex].classList.remove('active');
        indicators[currentIndex].classList.remove('active');
        
        // Atualizar índice atual
        currentIndex = index;
        
        // Adicionar classe active ao novo slide
        slides[currentIndex].classList.add('active');
        indicators[currentIndex].classList.add('active');
    }
    
    // Event listeners para os botões
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            stopSlideshow();
            prevSlide();
            startSlideshow();
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            stopSlideshow();
            nextSlide();
            startSlideshow();
        });
    }
    
    // Event listeners para os indicadores
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', function() {
            stopSlideshow();
            goToSlide(index);
            startSlideshow();
        });
    });
    
    // Pausar o slideshow quando o mouse estiver sobre ele
    const heroSection = document.querySelector('.hero');
    if (heroSection) {
        heroSection.addEventListener('mouseenter', stopSlideshow);
        heroSection.addEventListener('mouseleave', startSlideshow);
    }
}

// Função para ajustar a altura do hero de acordo com o conteúdo e tamanho da tela
function adjustHeroHeight() {
    const hero = document.querySelector('.hero');
    const heroContent = document.querySelector('.hero .container');
    const heroWave = document.querySelector('.hero-wave');
    const heroStats = document.querySelector('.hero-stats');
    
    if (!hero || !heroContent) return;
    
    // Definir altura mínima do hero com base no conteúdo
    const contentHeight = heroContent.offsetHeight;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    
    // Calcular altura do hero com base na relação de aspecto do dispositivo
    let heroHeight;
    
    if (windowWidth <= 576) {
        heroHeight = Math.max(contentHeight + 100, windowHeight * 0.5);
    } else if (windowWidth <= 768) {
        heroHeight = Math.max(contentHeight + 120, windowHeight * 0.6);
    } else if (windowWidth <= 992) {
        heroHeight = Math.max(contentHeight + 140, windowHeight * 0.7);
    } else {
        heroHeight = Math.max(contentHeight + 150, windowHeight * 0.8);
    }
    
    // Garantir espaço para as estatísticas
    if (heroStats) {
        const statsHeight = heroStats.offsetHeight;
        heroHeight = Math.max(heroHeight, contentHeight + statsHeight + 150);
    }
    
    // Limitar altura mínima absoluta
    heroHeight = Math.max(heroHeight, 400);
    
    // Aplicar altura ao hero
    hero.style.height = `${heroHeight}px`;
    
    // Ajustar a posição da onda para telas muito pequenas
    if (heroWave && windowWidth <= 576) {
        const scaleValue = Math.max(1.6, 800 / windowWidth);
        heroWave.querySelector('svg').style.transform = `scale(${scaleValue})`;
    }
    
    // Ajustar visibilidade das estatísticas em telas pequenas
    if (heroStats && windowWidth <= 576) {
        // Garantir que as estatísticas estejam visíveis
        heroStats.style.display = 'flex';
        heroStats.style.opacity = '1';
        
        // Ajustar posição vertical das estatísticas em telas muito pequenas
        if (windowHeight < 600) {
            heroStats.style.marginTop = '20px';
        }
    }
    
    // Atualizar posição dos slides
    const slides = document.querySelectorAll('.slide');
    slides.forEach(slide => {
        if (windowWidth < windowHeight) {
            // Em dispositivos de retrato, ajustar a posição da imagem
            slide.style.backgroundPosition = 'center center';
        } else {
            // Em dispositivos de paisagem, exibir mais do céu
            slide.style.backgroundPosition = 'center 25%';
        }
    });
}

// ========================================
// DOWNLOADS PAGE FUNCTIONALITY
// ========================================

// Dados dos arquivos disponíveis
const downloadsData = {
    'manual-seguranca': {
        title: 'Manual de Segurança',
        description: 'Guia completo de segurança para aventuras',
        filename: 'manual-seguranca.pdf'
    },
    'regulamento-geral': {
        title: 'Regulamento Geral',
        description: 'Regras e normas para participação',
        filename: 'regulamento-geral.pdf'
    },
    'video-seguranca': {
        title: 'Vídeo: Técnicas de Segurança',
        description: 'Tutorial completo sobre técnicas de segurança em aventuras',
        filename: 'video-tecnicas-seguranca.mp4'
    },
    'video-equipamentos': {
        title: 'Vídeo: Como Usar Equipamentos',
        description: 'Demonstração prática do uso correto dos equipamentos',
        filename: 'video-uso-equipamentos.mp4'
    },
    'fotos-equipamentos': {
        title: 'Pack Fotos: Equipamentos',
        description: 'Galeria com todos os equipamentos utilizados',
        filename: 'fotos-equipamentos.zip'
    },
    'fotos-tecnicas': {
        title: 'Pack Fotos: Técnicas',
        description: 'Imagens demonstrativas de técnicas de aventura',
        filename: 'fotos-tecnicas.zip'
    },
    'guia-equipamentos': {
        title: 'Guia de Equipamentos',
        description: 'Lista completa de equipamentos necessários',
        filename: 'guia-equipamentos.pdf'
    },
    'guia-trilhas': {
        title: 'Guia de Trilhas',
        description: 'Mapas e descrições detalhadas das trilhas',
        filename: 'guia-trilhas.pdf'
    },
    'ficha-inscricao': {
        title: 'Ficha de Inscrição',
        description: 'Formulário padrão para inscrição em aventuras',
        filename: 'ficha-inscricao.pdf'
    },
    'termo-responsabilidade': {
        title: 'Termo de Responsabilidade',
        description: 'Documento obrigatório para participação',
        filename: 'termo-responsabilidade.pdf'
    }
};

// Inicializar página de downloads
function initDownloadsPage() {
    // Verificar se estamos na página de downloads
    if (!document.querySelector('.downloads-grid')) {
        return;
    }

    // Inicializar funcionalidades
    initCategoryFilters();
    initDownloadModals();
    initDownloadButtons();
    initSearchFunctionality();
}

// Filtros de categoria (gerenciado pela função de pesquisa)
function initCategoryFilters() {
    // Esta função agora é gerenciada pela initSearchFunctionality()
    // Mantendo para compatibilidade, mas a lógica foi movida para lá
}

// Modais de download
function initDownloadModals() {
    const modal = document.getElementById('downloadModal');
    const successModal = document.getElementById('successModal');
    const closeBtn = document.querySelector('.close');
    
    if (!modal || !successModal) return;
    
    // Fechar modal ao clicar no X
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    // Fechar modal ao clicar fora dele
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
        if (event.target === successModal) {
            successModal.style.display = 'none';
        }
    });
    
    // Fechar modal com ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            if (modal.style.display === 'block') {
                modal.style.display = 'none';
            }
            if (successModal.style.display === 'block') {
                successModal.style.display = 'none';
            }
        }
    });
    
    // Formulário de download
    const downloadForm = document.getElementById('downloadForm');
    if (downloadForm) {
        downloadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validar formulário
            const formData = new FormData(this);
            const firstName = formData.get('firstName');
            const lastName = formData.get('lastName');
            const email = formData.get('email');
            const terms = formData.get('terms');
            
            if (!firstName || !lastName || !email || !terms) {
                alert('Por favor, preencha todos os campos obrigatórios e aceite os termos.');
                return;
            }
            
            // Simular envio dos dados
            console.log('Dados do cadastro:', {
                firstName,
                lastName,
                email,
                phone: formData.get('phone'),
                newsletter: formData.get('newsletter'),
                downloadItem: downloadForm.getAttribute('data-download-item')
            });
            
            // Fechar modal de cadastro
            modal.style.display = 'none';
            
            // Mostrar modal de sucesso
            successModal.style.display = 'block';
            
            // Simular download após 2 segundos
            setTimeout(() => {
                simulateDownload(downloadForm.getAttribute('data-download-item'));
            }, 2000);
            
            // Resetar formulário
            this.reset();
        });
    }
}

// Botões de download
function initDownloadButtons() {
    const downloadButtons = document.querySelectorAll('.download-btn');
    
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            
            const itemId = this.getAttribute('data-item');
            const itemData = downloadsData[itemId];
            
            if (itemData) {
                showDownloadModal(itemId, itemData);
            }
        });
    });
}

// Mostrar modal de download
function showDownloadModal(itemId, itemData) {
    const modal = document.getElementById('downloadModal');
    const downloadForm = document.getElementById('downloadForm');
    const titleElement = document.getElementById('downloadTitle');
    const descriptionElement = document.getElementById('downloadDescription');
    
    if (!modal || !downloadForm) return;
    
    // Atualizar informações do modal
    if (titleElement) titleElement.textContent = itemData.title;
    if (descriptionElement) descriptionElement.textContent = itemData.description;
    
    // Definir item no formulário
    downloadForm.setAttribute('data-download-item', itemId);
    
    // Mostrar modal
    modal.style.display = 'block';
}

// Simular download
function simulateDownload(itemId) {
    const itemData = downloadsData[itemId];
    
    if (itemData) {
        // Criar elemento de link temporário para simular download
        const link = document.createElement('a');
        link.href = '#'; // Em um sistema real, seria o link real do arquivo
        link.download = itemData.filename;
        link.style.display = 'none';
        
        // Simular o download (em produção, seria um link real)
        console.log(`Download iniciado: ${itemData.filename}`);
        
        // Mostrar notificação de download
        showDownloadNotification(itemData.title);
        
        document.body.appendChild(link);
        // link.click(); // Descomentado em produção
        document.body.removeChild(link);
    }
}

// Mostrar notificação de download
function showDownloadNotification(title) {
    // Criar notificação
    const notification = document.createElement('div');
    notification.className = 'download-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-download"></i>
            <span>Download de "${title}" iniciado!</span>
        </div>
    `;
    
    // Adicionar estilos
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--gradient-bg, linear-gradient(135deg, #229c43, #fe7d26));
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        z-index: 1001;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover após 4 segundos
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Fechar modal de sucesso
function closeSuccessModal() {
    const successModal = document.getElementById('successModal');
    if (successModal) {
        successModal.style.display = 'none';
    }
}

// Funcionalidade de pesquisa
function initSearchFunctionality() {
    const searchInput = document.getElementById('searchInput');
    const clearSearch = document.getElementById('clearSearch');
    const searchResults = document.getElementById('searchResults');
    const downloadItems = document.querySelectorAll('.download-item');
    const categoryButtons = document.querySelectorAll('.category-btn');
    
    if (!searchInput || !searchResults) return;
    
    let currentCategory = 'all';
    let searchTerm = '';
    
    // Função para filtrar itens
    function filterItems() {
        let visibleCount = 0;
        
        downloadItems.forEach(item => {
            const itemCategory = item.getAttribute('data-category');
            const title = item.querySelector('h3').textContent.toLowerCase();
            const description = item.querySelector('p').textContent.toLowerCase();
            const fileType = item.querySelector('.file-type').textContent.toLowerCase();
            
            // Verificar se o item atende aos critérios de categoria e pesquisa
            const matchesCategory = currentCategory === 'all' || itemCategory === currentCategory;
            const matchesSearch = searchTerm === '' || 
                title.includes(searchTerm) || 
                description.includes(searchTerm) || 
                fileType.includes(searchTerm);
            
            if (matchesCategory && matchesSearch) {
                showItem(item);
                visibleCount++;
            } else {
                hideItem(item);
            }
        });
        
        // Atualizar informações dos resultados
        updateSearchResults(visibleCount, searchTerm);
    }
    
    // Mostrar item com animação
    function showItem(item) {
        item.style.display = 'block';
        item.classList.remove('hidden');
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 50);
    }
    
    // Ocultar item com animação
    function hideItem(item) {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        setTimeout(() => {
            item.style.display = 'none';
            item.classList.add('hidden');
        }, 300);
    }
    
    // Atualizar texto dos resultados
    function updateSearchResults(count, term) {
        const totalItems = downloadItems.length;
        
        if (term === '' && currentCategory === 'all') {
            searchResults.textContent = 'Mostrando todos os materiais';
            searchResults.className = '';
        } else if (count === 0) {
            if (term !== '') {
                searchResults.textContent = `Nenhum resultado encontrado para "${term}"`;
            } else {
                searchResults.textContent = 'Nenhum item nesta categoria';
            }
            searchResults.className = 'no-results';
        } else {
            let message = `${count} de ${totalItems} materiais`;
            
            if (term !== '') {
                message += ` para "${term}"`;
            }
            
            if (currentCategory !== 'all') {
                const categoryName = getCategoryName(currentCategory);
                message += ` em ${categoryName}`;
            }
            
            searchResults.textContent = message;
            searchResults.className = 'searching';
        }
    }
    
    // Obter nome da categoria
    function getCategoryName(category) {
        const categoryNames = {
            'documents': 'Documentos',
            'videos': 'Vídeos', 
            'photos': 'Fotos',
            'guides': 'Guias',
            'forms': 'Formulários'
        };
        return categoryNames[category] || 'Todos';
    }
    
    // Event listener para pesquisa em tempo real
    searchInput.addEventListener('input', function() {
        searchTerm = this.value.toLowerCase().trim();
        const searchBox = this.parentElement;
        
        // Mostrar/ocultar botão de limpar
        if (searchTerm) {
            clearSearch.style.display = 'flex';
            this.classList.add('searching');
            searchBox.classList.add('active');
        } else {
            clearSearch.style.display = 'none';
            this.classList.remove('searching');
            searchBox.classList.remove('active');
        }
        
        // Filtrar com debounce
        clearTimeout(searchInput.searchTimeout);
        searchInput.searchTimeout = setTimeout(() => {
            filterItems();
        }, 300);
    });
    
    // Event listener para limpar pesquisa
    if (clearSearch) {
        clearSearch.addEventListener('click', function() {
            const searchBox = searchInput.parentElement;
            searchInput.value = '';
            searchTerm = '';
            this.style.display = 'none';
            searchInput.classList.remove('searching');
            searchBox.classList.remove('active');
            filterItems();
            searchInput.focus();
        });
    }
    
    // Atualizar filtros de categoria para trabalhar com a pesquisa
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            currentCategory = this.getAttribute('data-category');
            
            // Atualizar botão ativo
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filtrar itens
            filterItems();
        });
    });
    
    // Atalho de teclado para pesquisa (Ctrl+F ou Cmd+F)
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'f' && document.querySelector('.downloads-grid')) {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
        
        // ESC para limpar pesquisa
        if (e.key === 'Escape' && searchInput === document.activeElement) {
            if (searchInput.value) {
                const searchBox = searchInput.parentElement;
                searchInput.value = '';
                searchTerm = '';
                clearSearch.style.display = 'none';
                searchInput.classList.remove('searching');
                searchBox.classList.remove('active');
                filterItems();
            } else {
                searchInput.blur();
            }
        }
    });
}

// ========================================
// ADVENTURE PAGES FUNCTIONALITY
// ========================================

function initializeAdventurePage() {
    initializeHeroSlideshow();
    initializePhotoGallery();
    initializeVideoPlayer();
    initializeBookingForm();
}

// Hero Slideshow Functionality
function initializeHeroSlideshow() {
    const slideshow = document.querySelector('.hero-slideshow');
    if (!slideshow) return;

    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.hero-indicators .indicator');
    const prevBtn = document.querySelector('.hero-prev');
    const nextBtn = document.querySelector('.hero-next');
    
    if (slides.length === 0) return;

    let currentSlide = 0;
    let slideInterval;

    function showSlide(index) {
        // Remove active class from all slides and indicators
        slides.forEach(slide => slide.classList.remove('active'));
        indicators.forEach(indicator => indicator.classList.remove('active'));

        // Add active class to current slide and indicator
        slides[index].classList.add('active');
        if (indicators[index]) {
            indicators[index].classList.add('active');
        }

        currentSlide = index;
    }

    function nextSlide() {
        const next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }

    function prevSlide() {
        const prev = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prev);
    }

    function startSlideshow() {
        slideInterval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
    }

    function stopSlideshow() {
        clearInterval(slideInterval);
    }

    // Event listeners
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            nextSlide();
            stopSlideshow();
            startSlideshow(); // Restart auto-play
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            prevSlide();
            stopSlideshow();
            startSlideshow(); // Restart auto-play
        });
    }

    // Indicator clicks
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            showSlide(index);
            stopSlideshow();
            startSlideshow(); // Restart auto-play
        });
    });

    // Pause on hover
    slideshow.addEventListener('mouseenter', stopSlideshow);
    slideshow.addEventListener('mouseleave', startSlideshow);

    // Start the slideshow
    startSlideshow();
}

// Photo Gallery Functionality
function initializePhotoGallery() {
    const gallery = document.querySelector('.photo-gallery');
    if (!gallery) return;

    const mainPhoto = gallery.querySelector('.main-photo');
    const thumbnails = gallery.querySelectorAll('.thumbnail');
    const prevBtn = gallery.querySelector('.photo-prev');
    const nextBtn = gallery.querySelector('.photo-next');
    const currentCounter = gallery.querySelector('.current');
    const totalCounter = gallery.querySelector('.total');

    if (!mainPhoto || thumbnails.length === 0) return;

    let currentPhotoIndex = 0;
    const photoData = Array.from(thumbnails).map(thumb => ({
        src: thumb.querySelector('img').src,
        alt: thumb.querySelector('img').alt
    }));

    // Update total counter
    if (totalCounter) {
        totalCounter.textContent = photoData.length;
    }

    function showPhoto(index) {
        if (index < 0 || index >= photoData.length) return;

        // Update main photo
        mainPhoto.src = photoData[index].src;
        mainPhoto.alt = photoData[index].alt;

        // Update thumbnails
        thumbnails.forEach(thumb => thumb.classList.remove('active'));
        thumbnails[index].classList.add('active');

        // Update counter
        if (currentCounter) {
            currentCounter.textContent = index + 1;
        }

        currentPhotoIndex = index;
    }

    function nextPhoto() {
        const next = (currentPhotoIndex + 1) % photoData.length;
        showPhoto(next);
    }

    function prevPhoto() {
        const prev = (currentPhotoIndex - 1 + photoData.length) % photoData.length;
        showPhoto(prev);
    }

    // Event listeners
    if (nextBtn) {
        nextBtn.addEventListener('click', nextPhoto);
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', prevPhoto);
    }

    // Thumbnail clicks
    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', () => {
            showPhoto(index);
        });
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (gallery.matches(':hover')) {
            if (e.key === 'ArrowLeft') {
                prevPhoto();
            } else if (e.key === 'ArrowRight') {
                nextPhoto();
            }
        }
    });
}

// Video Player Functionality
function initializeVideoPlayer() {
    const videoPlaceholder = document.querySelector('.video-placeholder');
    if (!videoPlaceholder) return;

    videoPlaceholder.addEventListener('click', () => {
        showVideoModal();
    });

    function showVideoModal() {
        // Create and show video modal
        const modal = document.createElement('div');
        modal.className = 'video-modal';
        modal.innerHTML = `
            <div class="video-modal-content">
                <div class="video-modal-header">
                    <h3>Vídeo da Aventura</h3>
                    <button class="video-modal-close">&times;</button>
                </div>
                <div class="video-modal-body">
                    <div class="video-embed">
                        <p>🎬 Aqui seria exibido o vídeo da aventura</p>
                        <p>Integração com YouTube, Vimeo ou player personalizado</p>
                        <div class="video-placeholder-modal">
                            <i class="fas fa-video" style="font-size: 48px; color: #666;"></i>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add modal styles
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;

        const modalContent = modal.querySelector('.video-modal-content');
        modalContent.style.cssText = `
            background: white;
            border-radius: 15px;
            max-width: 800px;
            width: 90%;
            max-height: 90%;
            overflow: hidden;
        `;

        const modalHeader = modal.querySelector('.video-modal-header');
        modalHeader.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid #eee;
        `;

        const modalBody = modal.querySelector('.video-modal-body');
        modalBody.style.cssText = `
            padding: 40px;
            text-align: center;
        `;

        const videoPlaceholderModal = modal.querySelector('.video-placeholder-modal');
        videoPlaceholderModal.style.cssText = `
            background: #f8f9fa;
            padding: 60px;
            border-radius: 10px;
            margin-top: 20px;
        `;

        const closeBtn = modal.querySelector('.video-modal-close');
        closeBtn.style.cssText = `
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #666;
        `;

        // Close modal functionality
        closeBtn.addEventListener('click', () => {
            document.body.removeChild(modal);
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });

        document.addEventListener('keydown', function escapeHandler(e) {
            if (e.key === 'Escape') {
                document.body.removeChild(modal);
                document.removeEventListener('keydown', escapeHandler);
            }
        });

        document.body.appendChild(modal);
    }
}

// Booking Form Functionality
function initializeBookingForm() {
    // Esta função agora está desabilitada para permitir que o sistema Django de reservas funcione
    // O botão de reserva agora redireciona para o sistema completo de cadastro e pagamento
    
    // Apenas manter funcionalidade para links específicos do WhatsApp (não botões de reserva)
    const whatsappLinks = document.querySelectorAll('a[href*="wa.me"]');
    whatsappLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Permitir que links do WhatsApp funcionem normalmente
            // Não fazer preventDefault aqui
        });
    });
}

// Smooth scrolling for anchor links in adventure pages
document.addEventListener('click', (e) => {
    const target = e.target.closest('a[href^="#"]');
    if (!target) return;

    e.preventDefault();
    const targetId = target.getAttribute('href').substring(1);
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
        const headerHeight = document.querySelector('header').offsetHeight || 80;
        const targetPosition = targetElement.offsetTop - headerHeight;

        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
});

// Initialize adventure page functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeAdventurePage); 