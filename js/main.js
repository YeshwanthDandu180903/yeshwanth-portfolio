// Canvas Particle Animation
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Live Data Stream Animation Variables
let dataStreams = [];
let scrollY = 0;
let isScrolling = false;
let scrollTimeout;

window.addEventListener('scroll', () => {
    isScrolling = true;
    scrollY = window.scrollY;
    // Apply blur and darken effect based on scroll speed/position
    canvas.style.filter = `blur(${Math.min(scrollY / 200, 2)}px) brightness(${Math.max(1 - scrollY / 1500, 0.7)})`;

    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        isScrolling = false;
        canvas.style.filter = 'blur(0px) brightness(1)'; // Reset when stopped
    }, 150);
});

class DataSymbol {
    constructor(x, y, speed) {
        this.x = x;
        this.y = y;
        this.baseSpeed = speed; // Store original slow speed
        this.speed = speed;
        this.value = '';
        this.switchInterval = Math.floor(Math.random() * 20 + 20);
        this.frameCount = 0;
        this.opacity = Math.random() * 0.5 + 0.1;
        this.color = '#00f2c3'; // Base Teal
        this.text = ''; // Init in update
        this.aiMode = false;
        this.updateText(); // Initial text
    }

    updateText() {
        // Check current theme
        const theme = document.documentElement.getAttribute('data-theme') || 'dark';
        const isLight = theme === 'light';

        let symbols;
        if (isScrolling) {
            // AI Context on Scroll
            symbols = ['LLM', 'GPT', 'Neural', 'Tensor', 'RAG', 'Bias', 'Data', 'Model', 'AI', 'Deep', 'Net', 'Fit', 'Loss', 'Epoch'];
            this.aiMode = true;

            // Light Mode: Dark Teal, Dark Mode: White
            this.color = isLight ? '#004d40' : '#fff';
            this.opacity = Math.random() * 0.5 + 0.3; // Brighter
        } else {
            // Standard Math/Data
            symbols = ['0', '1', 'μ', 'σ', 'E[x]', 'Σ', 'p(y|x)', 'R²', 'acc', 'loss↓', 'AUC', '∫', '∂', '∅', '∞', 'ŷ', '∇'];
            this.aiMode = false;

            // Light Mode: Teal, Dark Mode: Cyan Accent
            this.color = isLight ? '#00796b' : '#00f2c3';
            this.opacity = Math.random() * 0.5 + 0.1;
        }
        this.text = symbols[Math.floor(Math.random() * symbols.length)];
    }

    update() {
        this.frameCount++;

        // Speed Adjustment
        // If scrolling, speed up very slightly (1.1x)
        this.speed = isScrolling ? this.baseSpeed * 1.1 : this.baseSpeed;

        if (this.frameCount >= this.switchInterval || (isScrolling && !this.aiMode) || (!isScrolling && this.aiMode)) {
            this.updateText();
            this.frameCount = 0;
        }

        this.y += this.speed;
        this.x += this.speed * 0.5; // Continue diagonal drift

        // Wrap around
        if (this.y > canvas.height) {
            this.y = Math.random() * -50;
            this.x = Math.random() * canvas.width;
            this.baseSpeed = Math.random() * 0.4 + 0.1;
        }
        if (this.x > canvas.width) {
            this.x = 0;
        }
    }

    draw() {
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.globalAlpha = this.opacity;
        ctx.font = this.aiMode ? 'bold 12px monospace' : '14px monospace';
        ctx.fillText(this.text, this.x, this.y);
        ctx.restore();
    }
}

function initParticles() {
    dataStreams = [];
    const columns = Math.floor(canvas.width / 80); // Wide spacing (80px)

    for (let i = 0; i < columns; i++) {
        const x = i * 80 + 40;
        // 1-3 symbols per column (Minimalist)
        const count = Math.floor(Math.random() * 3) + 1;
        for (let j = 0; j < count; j++) {
            dataStreams.push(new DataSymbol(x, Math.random() * canvas.height, Math.random() * 0.4 + 0.1));
        }
    }
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    dataStreams.forEach(stream => {
        stream.update();
        stream.draw();
    });

    requestAnimationFrame(animateParticles);
}

// Handle resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    initParticles();
});

// Start animation
initParticles();
animateParticles();

// DOM Elements
const navbar = document.querySelector('.navbar');
const typingTextElement = document.querySelector('.typing-text');
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('.nav-link');

// Typing Animation
// Typing Animation
const words = ["a Problem Solver", "a Data Analyst", "an Aspiring Data Scientist", "Aspiring for GenAI roles"];
let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typeSpeed = 100;

function typeEffect() {
    const currentWord = words[wordIndex];

    if (isDeleting) {
        typingTextElement.textContent = currentWord.substring(0, charIndex - 1);
        charIndex--;
        typeSpeed = 50;
    } else {
        typingTextElement.textContent = currentWord.substring(0, charIndex + 1);
        charIndex++;
        typeSpeed = 100;
    }

    if (!isDeleting && charIndex === currentWord.length) {
        isDeleting = true;
        typeSpeed = 2000; // Pause at end of word
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        wordIndex = (wordIndex + 1) % words.length;
        typeSpeed = 500; // Pause before new word
    }

    setTimeout(typeEffect, typeSpeed);
}

// Navbar Scroll Effect
function handleScroll() {
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
    } else {
        navbar.classList.remove('navbar-scrolled');
    }
}

// Intersection Observer for Scroll Animations
const observerOptions = {
    threshold: 0.2, // Trigger when 20% of element is visible
    rootMargin: "0px 0px -50px 0px"
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-active');
            observer.unobserve(entry.target); // Only animate once
        }
    });
}, observerOptions);

// Select elements to animate
document.querySelectorAll('.skill-card, .timeline-item, .project-card, .project-card-modern, .stat-box').forEach(el => {
    el.classList.add('fade-in-section'); // Add base class for CSS
    observer.observe(el);
});


// Active Link Highlighting
function highlightNavLink() {
    let scrollY = window.pageYOffset;

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight;
        const sectionTop = current.offsetTop - 100;
        const sectionId = current.getAttribute('id');

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href').includes(sectionId)) {
                    link.classList.add('active');
                }
            });
        }
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    typeEffect();
    typeCodeSnippet(); // Start Code Typing
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('scroll', highlightNavLink);
    window.addEventListener('scroll', revealElements); // Scroll Reveal

    // Initialize Observers
    initStatsObserver();
    initSkillsObserver();

    // Initialize EmailJS
    try {
        emailjs.init("YpTEACYMreCZL-Au7"); // User needs to replace this
    } catch (e) {
        console.log("EmailJS not configured yet");
    }

    // Contact Form Handler
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault();

            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = 'Sending... <i class="fas fa-spinner fa-spin ms-2"></i>';
            submitBtn.disabled = true;



            emailjs.sendForm('service_4plh5ub', 'template_ttokroj', this)
                .then(function () {
                    // Success
                    Swal.fire({
                        icon: 'success',
                        title: 'Message Sent!',
                        text: 'Thanks for reaching out! I will get back to you soon.',
                        background: '#1a1a1a',
                        color: '#fff',
                        confirmButtonColor: '#00f2c3'
                    });
                    contactForm.reset();
                }, function (error) {
                    // Error
                    console.log('FAILED...', error);
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Something went wrong. Please try again later.',
                        background: '#1a1a1a',
                        color: '#fff',
                        confirmButtonColor: '#d33'
                    });
                })
                .finally(function () {
                    submitBtn.innerHTML = originalBtnText;
                    submitBtn.disabled = false;
                });
        });
    }
});

// Theme Toggle
const themeToggleBtn = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

themeToggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);

    // Refresh animation colors immediately
    if (typeof dataStreams !== 'undefined') {
        dataStreams.forEach(stream => stream.updateText());
    }
});

function updateThemeIcon(theme) {
    if (theme === 'light') {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    } else {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
    }
}

// ==========================================
// NEW ANIMATIONS & FEATURES
// ==========================================

// 1. Code Snippet Typing Animation (Simulated HTML Typing)
const codeHTML = `
<span class="code-comment"># Building my future in AI</span><br>
<br>
<span class="code-def">while</span> <span class="code-var">learning</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="code-func">study</span>(<span class="code-str">"ML + DL"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="code-func">explore</span>(<span class="code-str">"Generative AI"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="code-func">build</span>(<span class="code-str">"Small Projects"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="code-func">stay_updated</span>(<span class="code-str">"AI Trends"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="code-func">share</span>(<span class="code-str">"Learning in Public"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="code-func">improve</span>()<br>
<br>
<span class="code-def">return</span> <span class="code-str">"Becoming 🚀"</span>
`;

function typeCodeSnippet() {
    const codeContainer = document.getElementById('code-typewriter');
    if (!codeContainer) return;

    const lines = codeHTML.split('<br>');

    function resetAndType() {
        codeContainer.innerHTML = '';
        let lineIndex = 0;

        function typeLine() {
            if (lineIndex < lines.length) {
                codeContainer.innerHTML += lines[lineIndex] + '<br>';
                lineIndex++;
                setTimeout(typeLine, 150); // 150ms per line (Much faster)
            } else {
                // Wait and loop
                setTimeout(resetAndType, 2000); // Wait 2s then restart
            }
        }
        typeLine();
    }

    resetAndType();
}

// 2. Stats Counter Animation
function initStatsObserver() {
    const statsSection = document.getElementById('stats-counter-section');
    if (!statsSection) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = statsSection.querySelectorAll('.counter-value');
                counters.forEach(counter => {
                    const target = +counter.parentElement.getAttribute('data-count');
                    const duration = 2000;
                    const increment = target / 50;

                    let current = 0;
                    const updateCount = () => {
                        current += increment;
                        if (current < target) {
                            counter.innerText = Math.ceil(current);
                            requestAnimationFrame(updateCount);
                        } else {
                            counter.innerText = target + "+";
                        }
                    };
                    updateCount();
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    observer.observe(statsSection);
}

// 3. Skill Bars Animation
function initSkillsObserver() {
    const skillsSection = document.getElementById('skills');
    if (!skillsSection) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBars = skillsSection.querySelectorAll('.progress-bar-animated');
                progressBars.forEach(bar => {
                    const width = bar.getAttribute('data-width');
                    bar.style.width = width;
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    observer.observe(skillsSection);
}

// 4. Scroll Reveal
function revealElements() {
    const reveals = document.querySelectorAll('.reveal');
    for (let i = 0; i < reveals.length; i++) {
        const windowHeight = window.innerHeight;
        const elementTop = reveals[i].getBoundingClientRect().top;
        const elementVisible = 150;

        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add('active');
        }
    }
}

// 5. Magnetic Cursor Effect
function initMagneticCursor() {
    const magnets = document.querySelectorAll('.btn, .social-icon, .nav-link');
    magnets.forEach((magnet) => {
        magnet.addEventListener('mousemove', function (e) {
            const position = magnet.getBoundingClientRect();
            const x = e.clientX - position.left - position.width / 2;
            const y = e.clientY - position.top - position.height / 2;

            magnet.style.transform = 'translate(' + x * 0.3 + 'px, ' + y * 0.5 + 'px)';
            magnet.style.transition = 'all 0s linear';
            magnet.classList.add('magnetic-active');
        });

        magnet.addEventListener('mouseleave', function (e) {
            magnet.style.transition = 'all 0.2s cubic-bezier(0, 0, 0.2, 1)';
            magnet.style.transform = 'translate(0px, 0px)';
            magnet.classList.remove('magnetic-active');
        });
    });
}

// Initialize Magnetic Cursor
document.addEventListener('DOMContentLoaded', () => {
    initMagneticCursor();
});
