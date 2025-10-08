// ===== MAIN APPLICATION ===== //
class CRMDemoApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupAnimations();
        this.setupParticles();
        this.setupCounters();
        this.setupFeatures();
        this.setupTechnology();
        this.setupSecurity();
        this.setupCalculator();
        this.setupScrollEffects();
        this.setupMobileMenu();
    }

    // ===== NAVIGATION ===== //
    setupNavigation() {
        const navbar = document.getElementById('navbar');
        const navLinks = document.querySelectorAll('.nav-link');
        
        // Scroll effect on navbar
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Smooth scroll for navigation links
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    targetSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
                
                // Update active link
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });

        // Update active link on scroll
        window.addEventListener('scroll', () => {
            let current = '';
            const sections = document.querySelectorAll('section[id]');
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop - 100;
                if (window.scrollY >= sectionTop) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });
    }

    // ===== MOBILE MENU ===== //
    setupMobileMenu() {
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.getElementById('nav-menu');
        
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });

        // Close menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }

    // ===== PARTICLES ANIMATION ===== //
    setupParticles() {
        const particlesContainer = document.getElementById('particles');
        const particleCount = 50;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: rgba(59, 130, 246, 0.3);
                border-radius: 50%;
                pointer-events: none;
            `;
            
            this.animateParticle(particle);
            particlesContainer.appendChild(particle);
        }
    }

    animateParticle(particle) {
        const resetParticle = () => {
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = '100%';
            particle.style.opacity = Math.random() * 0.5 + 0.2;
        };

        const animateUp = () => {
            particle.style.transition = `transform ${5 + Math.random() * 10}s linear`;
            particle.style.transform = `translateY(-${window.innerHeight + 100}px)`;
            
            setTimeout(() => {
                resetParticle();
                particle.style.transition = 'none';
                particle.style.transform = 'translateY(0)';
                setTimeout(animateUp, 100);
            }, (5 + Math.random() * 10) * 1000);
        };

        resetParticle();
        animateUp();
    }

    // ===== COUNTER ANIMATIONS ===== //
    setupCounters() {
        const counters = document.querySelectorAll('[data-count]');
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        counters.forEach(counter => observer.observe(counter));
    }

    animateCounter(element) {
        const target = parseFloat(element.dataset.count);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += step;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        };

        updateCounter();
    }

    // ===== FEATURES SECTION ===== //
    setupFeatures() {
        const featuresGrid = document.querySelector('.features-grid');
        
        const features = [
            {
                icon: '👤',
                title: 'Gestão de Usuários',
                description: 'Sistema completo de autenticação JWT com controle de perfis e permissões granulares. Gerencie equipes com segurança total.'
            },
            {
                icon: '💰',
                title: 'Orçamentos Inteligentes',
                description: 'Cálculos automáticos de rentabilidade, markup e comissões. Sistema avançado de precificação com análise de impostos.'
            },
            {
                icon: '📊',
                title: 'Dashboard Analítico',
                description: 'Métricas em tempo real, relatórios personalizados e insights estratégicos para tomada de decisões assertivas.'
            },
            {
                icon: '🔒',
                title: 'Segurança Enterprise',
                description: 'Criptografia de ponta, auditoria completa e conformidade com LGPD. Seus dados protegidos com padrão bancário.'
            },
            {
                icon: '⚡',
                title: 'Performance Otimizada',
                description: 'Arquitetura de microserviços com cache Redis. Resposta em menos de 50ms e 99.9% de disponibilidade.'
            },
            {
                icon: '🔄',
                title: 'Integração Total',
                description: 'APIs RESTful documentadas, webhooks e integrações nativas com principais ERPs e sistemas de pagamento.'
            }
        ];

        features.forEach((feature, index) => {
            const featureCard = document.createElement('div');
            featureCard.className = 'feature-card';
            featureCard.style.animationDelay = `${index * 0.1}s`;
            
            featureCard.innerHTML = `
                <div class="feature-icon">${feature.icon}</div>
                <h3 class="feature-title">${feature.title}</h3>
                <p class="feature-description">${feature.description}</p>
            `;
            
            featuresGrid.appendChild(featureCard);
        });

        this.setupScrollAnimation('.feature-card', 'fadeInUp');
    }

    // ===== TECHNOLOGY SECTION ===== //
    setupTechnology() {
        const techArchitecture = document.querySelector('.tech-architecture');
        
        const techStacks = [
            {
                title: 'Backend',
                technologies: [
                    { name: 'Python', description: 'Linguagem principal', icon: '🐍' },
                    { name: 'FastAPI', description: 'Framework web moderno', icon: '⚡' },
                    { name: 'SQLAlchemy', description: 'ORM avançado', icon: '🗃️' },
                    { name: 'Alembic', description: 'Migrações de banco', icon: '🔄' }
                ]
            },
            {
                title: 'Frontend',
                technologies: [
                    { name: 'React 18', description: 'Interface moderna', icon: '⚛️' },
                    { name: 'TypeScript', description: 'Type safety', icon: '📘' },
                    { name: 'Tailwind CSS', description: 'Styling utilitário', icon: '🎨' },
                    { name: 'Vite', description: 'Build tool rápido', icon: '⚡' }
                ]
            },
            {
                title: 'Infraestrutura',
                technologies: [
                    { name: 'PostgreSQL', description: 'Banco relacional', icon: '🐘' },
                    { name: 'Redis', description: 'Cache e mensageria', icon: '🔴' },
                    { name: 'Docker', description: 'Containerização', icon: '🐳' },
                    { name: 'Nginx', description: 'Proxy reverso', icon: '🌐' }
                ]
            },
            {
                title: 'DevOps',
                technologies: [
                    { name: 'AWS', description: 'Cloud computing', icon: '☁️' },
                    { name: 'GitHub Actions', description: 'CI/CD pipeline', icon: '🔄' },
                    { name: 'Monitoring', description: 'Observabilidade', icon: '📊' },
                    { name: 'Security', description: 'Proteção avançada', icon: '🛡️' }
                ]
            }
        ];

        techStacks.forEach((stack, index) => {
            const stackElement = document.createElement('div');
            stackElement.className = 'tech-stack';
            stackElement.style.animationDelay = `${index * 0.2}s`;
            
            const techList = stack.technologies.map(tech => `
                <li class="tech-item">
                    <div class="tech-item-icon">${tech.icon}</div>
                    <div class="tech-item-info">
                        <div class="tech-item-name">${tech.name}</div>
                        <div class="tech-item-description">${tech.description}</div>
                    </div>
                </li>
            `).join('');
            
            stackElement.innerHTML = `
                <h3 class="tech-stack-title">${stack.title}</h3>
                <ul class="tech-list">${techList}</ul>
            `;
            
            techArchitecture.appendChild(stackElement);
        });

        this.setupScrollAnimation('.tech-stack', 'slideInLeft');
    }

    // ===== SECURITY SECTION ===== //
    setupSecurity() {
        const securityFeatures = document.querySelector('.security-features');
        
        const securities = [
            {
                icon: '🔐',
                title: 'Autenticação JWT',
                description: 'Tokens seguros com expiração automática e refresh tokens para máxima segurança de acesso.'
            },
            {
                icon: '🛡️',
                title: 'Criptografia AES-256',
                description: 'Dados sensíveis protegidos com criptografia militar. Chaves rotacionadas automaticamente.'
            },
            {
                icon: '📋',
                title: 'Auditoria Completa',
                description: 'Log detalhado de todas as ações. Rastreabilidade total para conformidade e investigações.'
            },
            {
                icon: '🔍',
                title: 'Monitoramento 24/7',
                description: 'Detecção de anomalias em tempo real. Alertas automáticos para tentativas de invasão.'
            },
            {
                icon: '⚖️',
                title: 'Conformidade LGPD',
                description: 'Implementação completa da Lei Geral de Proteção de Dados. Direitos dos titulares garantidos.'
            },
            {
                icon: '🔄',
                title: 'Backup Automático',
                description: 'Backups criptografados a cada 6 horas. Recuperação de desastres em menos de 1 hora.'
            }
        ];

        securities.forEach((security, index) => {
            const securityElement = document.createElement('div');
            securityElement.className = 'security-feature';
            securityElement.style.animationDelay = `${index * 0.1}s`;
            
            securityElement.innerHTML = `
                <div class="security-icon">${security.icon}</div>
                <h3 class="security-title">${security.title}</h3>
                <p class="security-description">${security.description}</p>
            `;
            
            securityFeatures.appendChild(securityElement);
        });

        this.setupScrollAnimation('.security-feature', 'fadeInUp');
    }

    // ===== AWS CALCULATOR ===== //
    setupCalculator() {
        const calculatorContainer = document.querySelector('.calculator-container');
        
        calculatorContainer.innerHTML = `
            <form class="calculator-form" id="aws-calculator">
                <div class="form-group">
                    <label class="form-label">Número de Usuários</label>
                    <input type="number" class="form-input" id="users" value="10" min="1" max="1000">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Orçamentos por Mês</label>
                    <input type="number" class="form-input" id="budgets" value="100" min="10" max="10000">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Região AWS</label>
                    <select class="form-select" id="region">
                        <option value="us-east-1">US East (N. Virginia)</option>
                        <option value="sa-east-1" selected>South America (São Paulo)</option>
                        <option value="eu-west-1">Europe (Ireland)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Tipo de Instância</label>
                    <select class="form-select" id="instance">
                        <option value="t3.micro">t3.micro (1 vCPU, 1GB RAM)</option>
                        <option value="t3.small" selected>t3.small (2 vCPU, 2GB RAM)</option>
                        <option value="t3.medium">t3.medium (2 vCPU, 4GB RAM)</option>
                        <option value="t3.large">t3.large (2 vCPU, 8GB RAM)</option>
                    </select>
                </div>
            </form>
            
            <div class="calculator-results" id="calculator-results">
                <h3 class="results-title">Estimativa de Custos Mensais</h3>
                <div class="results-grid" id="results-grid">
                    <!-- Results will be populated here -->
                </div>
            </div>
        `;

        // Setup calculator logic
        const form = document.getElementById('aws-calculator');
        const inputs = form.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', () => this.calculateAWSCosts());
        });

        // Initial calculation
        this.calculateAWSCosts();
    }

    calculateAWSCosts() {
        const users = parseInt(document.getElementById('users').value) || 10;
        const budgets = parseInt(document.getElementById('budgets').value) || 100;
        const region = document.getElementById('region').value;
        const instance = document.getElementById('instance').value;

        // AWS pricing (simplified, in USD)
        const pricing = {
            instances: {
                't3.micro': { hourly: 0.0104, monthly: 7.59 },
                't3.small': { hourly: 0.0208, monthly: 15.18 },
                't3.medium': { hourly: 0.0416, monthly: 30.37 },
                't3.large': { hourly: 0.0832, monthly: 60.74 }
            },
            rds: {
                't3.micro': { monthly: 15.73 },
                't3.small': { monthly: 31.46 },
                't3.medium': { monthly: 62.93 },
                't3.large': { monthly: 125.86 }
            },
            elasticache: {
                't3.micro': { monthly: 11.59 },
                't3.small': { monthly: 23.18 },
                't3.medium': { monthly: 46.37 },
                't3.large': { monthly: 92.74 }
            }
        };

        // Calculate costs based on usage
        const instanceCost = pricing.instances[instance].monthly * 2; // 2 instances (user + budget service)
        const rdsCost = pricing.rds[instance].monthly;
        const redisCost = pricing.elasticache[instance].monthly;
        const loadBalancerCost = 22.27; // ALB cost
        const storageCost = Math.max(20, budgets * 0.1); // EBS storage
        const backupCost = storageCost * 0.5; // Backup storage
        
        // Regional multiplier
        const regionalMultiplier = region === 'sa-east-1' ? 1.2 : region === 'eu-west-1' ? 1.1 : 1.0;
        
        const subtotal = (instanceCost + rdsCost + redisCost + loadBalancerCost + storageCost + backupCost) * regionalMultiplier;
        const support = subtotal * 0.1; // 10% for support
        const total = subtotal + support;

        // Convert to BRL (approximate)
        const usdToBrl = 5.2;
        const totalBRL = total * usdToBrl;

        this.displayResults({
            instances: instanceCost * regionalMultiplier,
            database: rdsCost * regionalMultiplier,
            cache: redisCost * regionalMultiplier,
            loadBalancer: loadBalancerCost * regionalMultiplier,
            storage: storageCost * regionalMultiplier,
            backup: backupCost * regionalMultiplier,
            support: support,
            totalUSD: total,
            totalBRL: totalBRL,
            perUser: totalBRL / users,
            perBudget: totalBRL / budgets
        });
    }

    displayResults(costs) {
        const resultsGrid = document.getElementById('results-grid');
        
        const results = [
            { label: 'Instâncias EC2', value: `$${costs.instances.toFixed(2)}` },
            { label: 'Banco RDS', value: `$${costs.database.toFixed(2)}` },
            { label: 'Cache Redis', value: `$${costs.cache.toFixed(2)}` },
            { label: 'Load Balancer', value: `$${costs.loadBalancer.toFixed(2)}` },
            { label: 'Armazenamento', value: `$${costs.storage.toFixed(2)}` },
            { label: 'Backup', value: `$${costs.backup.toFixed(2)}` },
            { label: 'Total USD', value: `$${costs.totalUSD.toFixed(2)}` },
            { label: 'Total BRL', value: `R$ ${costs.totalBRL.toFixed(2)}` },
            { label: 'Por Usuário', value: `R$ ${costs.perUser.toFixed(2)}` },
            { label: 'Por Orçamento', value: `R$ ${costs.perBudget.toFixed(2)}` }
        ];

        resultsGrid.innerHTML = results.map(result => `
            <div class="result-item">
                <span class="result-value">${result.value}</span>
                <span class="result-label">${result.label}</span>
            </div>
        `).join('');
    }

    // ===== SCROLL ANIMATIONS ===== //
    setupScrollAnimation(selector, animationClass) {
        const elements = document.querySelectorAll(selector);
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = `${animationClass} 0.6s ease forwards`;
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        elements.forEach(element => {
            element.style.opacity = '0';
            observer.observe(element);
        });
    }

    setupScrollEffects() {
        // Parallax effect for hero section
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const heroVisual = document.querySelector('.hero-visual');
            
            if (heroVisual) {
                heroVisual.style.transform = `translateY(${scrolled * 0.1}px)`;
            }
        });

        // Scroll to top functionality
        const scrollIndicator = document.querySelector('.scroll-indicator');
        if (scrollIndicator) {
            scrollIndicator.addEventListener('click', () => {
                document.querySelector('#features').scrollIntoView({
                    behavior: 'smooth'
                });
            });
        }
    }

    setupAnimations() {
        // Add CSS animations dynamically
        const style = document.createElement('style');
        style.textContent = `
            .fadeInUp {
                animation: fadeInUp 0.6s ease forwards;
            }
            
            .slideInLeft {
                animation: slideInLeft 0.6s ease forwards;
            }
            
            .slideInRight {
                animation: slideInRight 0.6s ease forwards;
            }
        `;
        document.head.appendChild(style);
    }
}

// ===== UTILITY FUNCTIONS ===== //
function debounce(func, wait) {
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

function throttle(func, limit) {
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

// ===== INITIALIZATION ===== //
document.addEventListener('DOMContentLoaded', () => {
    new CRMDemoApp();
    
    // Add loading animation
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// ===== ERROR HANDLING ===== //
window.addEventListener('error', (e) => {
    console.error('Application error:', e.error);
});

// ===== PERFORMANCE MONITORING ===== //
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}