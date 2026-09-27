document.addEventListener('DOMContentLoaded', function () {

    /* ============================================================
       LIVE CLOCK + GREETING
    ============================================================ */
    function updateClock() {
        const now = new Date();

        const hh = String(now.getHours()).padStart(2, '0');
        const mm = String(now.getMinutes()).padStart(2, '0');
        const ss = String(now.getSeconds()).padStart(2, '0');

        const clockEl = document.getElementById('liveClock');
        if (clockEl) clockEl.textContent = `${hh}:${mm}:${ss}`;

        const dateEl = document.getElementById('liveDate');
        if (dateEl) {
            const options = { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' };
            dateEl.textContent = now.toLocaleDateString('en-US', options);
        }

        const greetEl = document.getElementById('greeting');
        if (greetEl) {
            const h = now.getHours();
            let greet = '👋 Welcome back, Admin';
            if (h < 12)      greet = '🌅 Good Morning, Admin';
            else if (h < 17) greet = '☀️ Good Afternoon, Admin';
            else if (h < 21) greet = '🌆 Good Evening, Admin';
            else             greet = '🌙 Good Night, Admin';
            greetEl.textContent = greet;
        }
    }
    updateClock();
    setInterval(updateClock, 1000);

    /* ============================================================
       ANIMATED COUNTERS
    ============================================================ */
    document.querySelectorAll('[data-count]').forEach(el => {
        const target = parseInt(el.dataset.count) || 0;
        if (target === 0) { el.textContent = '0'; return; }
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 40));
        const timer = setInterval(() => {
            current += step;
            if (current >= target) { current = target; clearInterval(timer); }
            el.textContent = current;
        }, 25);
    });

    /* ============================================================
       PROGRESS BARS
    ============================================================ */
    setTimeout(() => {
        document.querySelectorAll('.rank-fill').forEach(el => {
            el.style.width = (el.dataset.pct || 0) + '%';
        });
    }, 200);

    /* ============================================================
       SCROLL REVEAL
    ============================================================ */
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.style.opacity = '1';
                e.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.05 });

    document.querySelectorAll('.feature-tile, .stat-card, .panel, .hero').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(25px)';
        el.style.transition = 'opacity 0.7s ease, transform 0.7s ease';
        observer.observe(el);
    });

    /* ============================================================
       HERO 3D TILT EFFECT
    ============================================================ */
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.addEventListener('mousemove', (e) => {
            const rect = hero.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width  - 0.5;
            const y = (e.clientY - rect.top)  / rect.height - 0.5;
            hero.style.transform = `perspective(1000px) rotateY(${x * 4}deg) rotateX(${-y * 4}deg)`;
        });
        hero.addEventListener('mouseleave', () => {
            hero.style.transform = 'perspective(1000px) rotateY(0) rotateX(0)';
        });
    }

    /* ============================================================
       BUTTON RIPPLE EFFECT
    ============================================================ */
    document.querySelectorAll('button, .cta-btn, .feature-tile').forEach(btn => {
        btn.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top  = (e.clientY - rect.top  - size / 2) + 'px';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 700);
        });
    });

});