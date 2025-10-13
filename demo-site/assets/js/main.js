/**
 * Loen CRM - Main JavaScript
 * Sistema de CRM minimalista e profissional
 */

class LoenApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupScrollAnimations();
        this.setupContactForm();
        this.setupSmoothScrolling();
        this.setupMobileMenu();
        this.setupAnimations();
    }

    /**
     * Configuração da navegação
     */
    setupNavigation() {
        const navbar = document.querySelector('.navbar');
        
        if (!navbar) return;

        // Efeito de scroll na navbar
        window.addEventListener('scroll', this.throttle(() => {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                navbar.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.1)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.boxShadow = 'none';
            }
        }, 100));
    }

    /**
     * Configuração do menu mobile
     */
    setupMobileMenu() {
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (!navToggle || !navMenu) return;

        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });

        // Fechar menu ao clicar em um link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }

    /**
     * Configuração de scroll suave
     */
    setupSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const targetId = link.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - 70; // Altura da navbar
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * Configuração das animações de scroll
     */
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                }
            });
        }, observerOptions);

        // Observar elementos que devem ser animados
        const animatedElements = document.querySelectorAll(
            '.benefit-card, .feature-item, .section-header, .hero-content'
        );
        
        animatedElements.forEach(el => {
            observer.observe(el);
        });
    }

    /**
     * Configuração do formulário de contato
     */
    setupContactForm() {
        const form = document.querySelector('.contact-form');
        
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            // Validação básica
            if (!this.validateForm(data)) {
                this.showMessage('Por favor, preencha todos os campos obrigatórios.', 'error');
                return;
            }

            // Simular envio do formulário
            this.submitForm(data);
        });

        // Validação em tempo real
        const inputs = form.querySelectorAll('.form-input');
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });
    }

    /**
     * Validação do formulário
     */
    validateForm(data) {
        const required = ['name', 'email', 'message'];
        return required.every(field => data[field] && data[field].trim() !== '');
    }

    /**
     * Validação de campo individual
     */
    validateField(input) {
        const value = input.value.trim();
        const isValid = value !== '';
        
        if (input.type === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const isValidEmail = emailRegex.test(value);
            this.toggleFieldError(input, !isValidEmail);
            return isValidEmail;
        }
        
        this.toggleFieldError(input, !isValid);
        return isValid;
    }

    /**
     * Toggle erro no campo
     */
    toggleFieldError(input, hasError) {
        if (hasError) {
            input.style.borderColor = '#ef4444';
            input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
        } else {
            input.style.borderColor = '#d4d4d4';
            input.style.boxShadow = 'none';
        }
    }

    /**
     * Envio do formulário
     */
    async submitForm(data) {
        const submitBtn = document.querySelector('.contact-form .btn-primary');
        const originalText = submitBtn.textContent;
        
        // Estado de loading
        submitBtn.textContent = 'Enviando...';
        submitBtn.disabled = true;
        
        try {
            // Simular delay de envio
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Aqui você integraria com seu backend
            console.log('Dados do formulário:', data);
            
            this.showMessage('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success');
            document.querySelector('.contact-form').reset();
            
        } catch (error) {
            console.error('Erro ao enviar formulário:', error);
            this.showMessage('Erro ao enviar mensagem. Tente novamente.', 'error');
        } finally {
            // Restaurar botão
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }

    /**
     * Exibir mensagem de feedback
     */
    showMessage(message, type = 'info') {
        // Remover mensagem anterior se existir
        const existingMessage = document.querySelector('.form-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        const messageEl = document.createElement('div');
        messageEl.className = `form-message form-message--${type}`;
        messageEl.textContent = message;
        
        // Estilos da mensagem
        Object.assign(messageEl.style, {
            padding: '1rem',
            borderRadius: '0.5rem',
            marginTop: '1rem',
            fontSize: '0.875rem',
            fontWeight: '500',
            backgroundColor: type === 'success' ? '#f0f9ff' : '#fef2f2',
            color: type === 'success' ? '#0369a1' : '#dc2626',
            border: `1px solid ${type === 'success' ? '#0ea5e9' : '#ef4444'}`
        });

        const form = document.querySelector('.contact-form');
        form.appendChild(messageEl);

        // Remover mensagem após 5 segundos
        setTimeout(() => {
            messageEl.remove();
        }, 5000);
    }

    /**
     * Configuração de animações gerais
     */
    setupAnimations() {
        // Animação dos cards de benefícios
        const benefitCards = document.querySelectorAll('.benefit-card');
        benefitCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });

        // Animação dos botões
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.transform = 'translateY(-2px)';
            });
            
            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translateY(0)';
            });
        });

        // Animação do mockup do dashboard
        const dashboardMockup = document.querySelector('.dashboard-mockup');
        if (dashboardMockup) {
            this.animateDashboard();
        }
    }

    /**
     * Animação do mockup do dashboard
     */
    animateDashboard() {
        const sidebarItems = document.querySelectorAll('.sidebar-item');
        const chartArea = document.querySelector('.chart-area');
        const statCards = document.querySelectorAll('.stat-card');

        // Animação dos itens da sidebar
        setInterval(() => {
            sidebarItems.forEach((item, index) => {
                setTimeout(() => {
                    item.classList.toggle('active');
                }, index * 200);
            });
        }, 3000);

        // Animação da área do gráfico
        if (chartArea) {
            setInterval(() => {
                chartArea.style.background = chartArea.style.background === 'linear-gradient(45deg, #0ea5e9 0%, #0284c7 100%)' 
                    ? '#f5f5f5' 
                    : 'linear-gradient(45deg, #0ea5e9 0%, #0284c7 100%)';
            }, 2000);
        }

        // Animação dos cards de estatística
        statCards.forEach((card, index) => {
            setInterval(() => {
                card.style.background = card.style.background === 'linear-gradient(45deg, #0ea5e9 0%, #0284c7 100%)' 
                    ? '#f5f5f5' 
                    : 'linear-gradient(45deg, #0ea5e9 0%, #0284c7 100%)';
            }, 1500 + (index * 300));
        });
    }

    /**
     * Utility: Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }

    /**
     * Utility: Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Inicializar aplicação quando DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new LoenApp();
});

// Tratamento de erros globais
window.addEventListener('error', (e) => {
    console.error('Erro na aplicação:', e.error);
});

// Otimização de performance
window.addEventListener('load', () => {
    // Lazy loading de imagens se necessário
    const images = document.querySelectorAll('img[data-src]');
    if (images.length > 0) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }
});