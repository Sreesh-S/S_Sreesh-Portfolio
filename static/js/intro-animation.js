/* -------------------------------------------------------------
   CINEMATIC SCREEN-FILLING CODE STREAM INTRO ANIMATION (60 FPS HIGH-PERFORMANCE)
   ------------------------------------------------------------- */

(function() {
    'use strict';

    function startIntro() {
        if (window.location.pathname.includes('/admin')) return;
        const introContainer = document.getElementById('cinematic-intro');
        if (!introContainer) return;

        introContainer.style.display = 'flex';
        introContainer.style.opacity = '1';

        initCinematicIntro(introContainer);
    }

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        setTimeout(startIntro, 10);
    } else {
        document.addEventListener('DOMContentLoaded', startIntro);
        window.addEventListener('load', startIntro);
    }

    function initCinematicIntro(container) {
        const canvas = document.getElementById('intro-canvas');
        const typography = document.getElementById('intro-typography');
        const line1 = document.getElementById('intro-welcome-1');
        const line2 = document.getElementById('intro-welcome-2');
        const skipHint = document.getElementById('intro-skip-hint');
        if (!canvas || !typography || !line1 || !line2) return;

        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        let cX = width / 2;
        let cY = height / 2;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            cX = width / 2;
            cY = height / 2;
        });

        // Hacker Matrix Green Code Snippet Vocabulary
        const HACKER_GREEN_PALETTE = ['#39FF14', '#00FF66', '#00FF41', '#10B981', '#7CFF00', '#20C997'];

        const CODE_SNIPPETS = [
            { text: 'def build_future():', color: '#39FF14' },
            { text: 'return "innovation"', color: '#00FF66' },
            { text: 'class Developer:', color: '#00FF41' },
            { text: 'import django', color: '#39FF14' },
            { text: 'from django.shortcuts import render', color: '#00FF66' },
            { text: 'def portfolio(request):', color: '#10B981' },
            { text: 'return render(request, "home.html")', color: '#39FF14' },
            { text: 'const create = () => {}', color: '#7CFF00' },
            { text: 'SELECT ideas FROM imagination', color: '#00FF66' },
            { text: 'WHERE possible = TRUE;', color: '#39FF14' },
            { text: 'git add .', color: '#00FF41' },
            { text: 'git commit -m "awesome"', color: '#39FF14' },
            { text: 'git push origin main', color: '#00FF66' },
            { text: 'python manage.py runserver', color: '#39FF14' },
            { text: 'request.POST.get()', color: '#10B981' },
            { text: 'models.Model', color: '#7CFF00' },
            { text: 'objects.filter(is_active=True)', color: '#39FF14' },
            { text: '127.0.0.1:8000', color: '#00FF66' },
            { text: 'HTTP 200 OK', color: '#39FF14' },
            { text: 'Scikit-learn', color: '#00FF41' },
            { text: 'Pandas.DataFrame()', color: '#10B981' },
            { text: 'NumPy.array()', color: '#7CFF00' },
            { text: 'RandomForestClassifier()', color: '#39FF14' },
            { text: 'OCR.parse_pdf()', color: '#00FF66' },
            { text: '0x01', color: '#00FF41' },
            { text: '0xFF', color: '#39FF14' },
            { text: '{}', color: '#39FF14' },
            { text: '[]', color: '#00FF66' },
            { text: '()', color: '#00FF41' },
            { text: '<>', color: '#10B981' },
            { text: '=>', color: '#39FF14' },
            { text: '&&', color: '#00FF66' },
            { text: '||', color: '#7CFF00' },
            { text: '==', color: '#00FF41' },
            { text: '===', color: '#39FF14' },
            { text: 'npm run dev', color: '#00FF66' },
            { text: 'CSRFToken', color: '#10B981' },
            { text: 'Response.json()', color: '#39FF14' },
            { text: 'print("Hello World")', color: '#39FF14' },
            { text: 'System check identified no issues', color: '#39FF14' },
            { text: '3D Mesh Shaders', color: '#00FF66' },
            { text: 'WebGL Canvas', color: '#00FF41' },
            { text: 'S Sreesh', color: '#39FF14' }
        ];

        // 3D Fragment Engine State
        let fragments = [];
        let sparks = [];
        let scenePhase = 0; // 0=Dark, 1=Typing, 2=FillWindow, 3=Tunnel, 4=Reveal, 5=Done
        let animFrameId = null;
        let isSkipping = false;

        // Mouse Interactive Physics
        let mouseX = cX;
        let mouseY = cY;
        window.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        // Ultra-smooth 60FPS fragment count allocation
        const fragmentCount = width < 576 ? 75 : (width < 992 ? 110 : 150);

        // Ultra-Fast 3D Code Fragment Class
        class CodeFragment {
            constructor() {
                this.init();
            }

            init() {
                const item = CODE_SNIPPETS[Math.floor(Math.random() * CODE_SNIPPETS.length)];
                this.text = item.text;
                this.color = item.color;

                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.z = Math.random() * 1000;

                this.vx = (Math.random() - 0.5) * 1.2;
                this.vy = (Math.random() - 0.5) * 1.2;
                this.vz = -2 - Math.random() * 4;

                this.layer = Math.floor(Math.random() * 3);
                this.fontSize = this.layer === 2 ? 18 : (this.layer === 1 ? 14 : 10);
                this.opacity = this.layer === 2 ? 0.95 : (this.layer === 1 ? 0.65 : 0.4);
            }

            update(warpSpeed = 1) {
                this.x += this.vx * warpSpeed;
                this.y += this.vy * warpSpeed;
                this.z += this.vz * warpSpeed;

                // Mouse repulsion force
                const dx = this.x - mouseX;
                const dy = this.y - mouseY;
                const distSq = dx * dx + dy * dy;
                if (distSq < 25000 && distSq > 0) {
                    const dist = Math.sqrt(distSq);
                    this.x += (dx / dist) * 1.5;
                    this.y += (dy / dist) * 1.5;
                }

                // Recycle offscreen
                if (this.z < -100 || this.x < -150 || this.x > width + 150 || this.y < -150 || this.y > height + 150) {
                    if (scenePhase < 4) {
                        this.init();
                        this.z = 1000;
                    }
                }
            }

            draw() {
                const focalLength = 400;
                const scale = focalLength / Math.max(10, (focalLength + this.z));
                const projX = (this.x - cX) * scale + cX;
                const projY = (this.y - cY) * scale + cY;

                if (projX < -150 || projX > width + 150 || projY < -150 || projY > height + 150) return;

                const currentFontSize = Math.round(Math.max(9, Math.min(32, this.fontSize * scale)));
                ctx.font = `${this.layer === 2 ? '700' : '500'} ${currentFontSize}px 'Fira Code', monospace`;
                
                const depthAlpha = Math.min(1, Math.max(0.15, (1200 - this.z) / 1200)) * this.opacity;
                ctx.globalAlpha = depthAlpha;
                ctx.fillStyle = this.color;
                ctx.fillText(this.text, projX, projY);
            }
        }

        // Energy Sparks
        class EnergySpark {
            constructor() {
                this.x = cX + (Math.random() - 0.5) * 300;
                this.y = cY + (Math.random() - 0.5) * 100;
                this.vx = (Math.random() - 0.5) * 3;
                this.vy = (Math.random() - 0.5) * 3;
                this.size = Math.random() * 2 + 1;
                this.life = 1;
                this.decay = 0.04;
                this.color = Math.random() > 0.5 ? '#39FF14' : '#00FF66';
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                this.life -= this.decay;
            }

            draw() {
                if (this.life <= 0) return;
                ctx.globalAlpha = this.life;
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        // MASTER TIMELINE CONTROLLER
        function runMasterTimeline() {
            // SCENE 1 (0.0s - 0.2s): Dark Opening & Cursor Typing
            setTimeout(() => {
                scenePhase = 1;
                typeWriterText();
            }, 200);

            // SCENE 2 (2.8s): Hold Welcome Message longer, then Fill Window with Code
            setTimeout(() => {
                if (scenePhase >= 2) return;
                triggerFillWindowWithCode();
            }, 2800);
        }

        // SCENE 1: Clean Typography Reveal
        function typeWriterText() {
            line1.innerText = "WELCOME TO";
            line2.innerText = "MY DIGITAL DOMAIN";
            line1.style.opacity = '1';
            line2.style.opacity = '1';
        }

        function spawnEnergySparks() {
            if (scenePhase !== 2) return;
            for (let i = 0; i < 2; i++) {
                sparks.push(new EnergySpark());
            }
            setTimeout(spawnEnergySparks, 80);
        }

        // SCENE 2: Fill Window with Code & Transition
        function triggerFillWindowWithCode() {
            if (scenePhase >= 2) return;
            scenePhase = 2;

            if (skipHint) skipHint.style.opacity = '1';
            spawnEnergySparks();

            // Populate screen-filling code stream across the entire window
            fragments = [];
            for (let i = 0; i < fragmentCount; i++) {
                fragments.push(new CodeFragment());
            }

            // Smoothly dissolve welcome typography into code space after 1.5s
            setTimeout(() => {
                typography.style.opacity = '0';
                typography.style.transition = 'opacity 1s ease';
            }, 1500);

            // SCENE 3: Accelerate into 3D Code Space Tunnel
            setTimeout(() => {
                scenePhase = 3;
                fragments.forEach(f => {
                    f.vz = -12 - Math.random() * 18; // Accelerate toward camera
                });
            }, 2000);

            // SCENE 4 (3.8s): Reveal Portfolio Website
            setTimeout(() => {
                scenePhase = 4;
                container.style.opacity = '0';
                setTimeout(finishIntro, 600);
            }, 2400);
        }

        // Interactive Click on Welcome Text
        typography.addEventListener('click', () => {
            if (scenePhase < 2) {
                triggerFillWindowWithCode();
            }
        });

        // Fast Skip (ESC / Space / Enter)
        function performSkip() {
            if (isSkipping || scenePhase === 5) return;
            isSkipping = true;
            container.style.opacity = '0';
            setTimeout(finishIntro, 350);
        }

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' || e.key === ' ' || e.key === 'Enter') {
                performSkip();
            }
        });

        if (skipHint) {
            skipHint.addEventListener('click', performSkip);
        }

        // Finish Intro & Mount Website
        function finishIntro() {
            scenePhase = 5;
            if (animFrameId) cancelAnimationFrame(animFrameId);
            container.style.display = 'none';

            // Trigger main site GSAP intro animations
            if (window.playIntroAnimations) {
                window.playIntroAnimations();
            }

            // Refresh ScrollTrigger positions and force content visibility
            setTimeout(() => {
                if (typeof ScrollTrigger !== 'undefined') {
                    ScrollTrigger.refresh();
                }
                window.dispatchEvent(new Event('scroll'));
            }, 100);
        }

        // MAIN CANVAS RENDER LOOP (OPTIMIZED FOR 60 FPS)
        function renderLoop() {
            ctx.clearRect(0, 0, width, height);

            if (scenePhase === 2) {
                for (let idx = sparks.length - 1; idx >= 0; idx--) {
                    const s = sparks[idx];
                    s.update();
                    s.draw();
                    if (s.life <= 0) sparks.splice(idx, 1);
                }
            }

            if (scenePhase >= 2 && scenePhase < 5) {
                const warpMultiplier = scenePhase === 3 ? 1.6 : 1;
                for (let i = 0; i < fragments.length; i++) {
                    fragments[i].update(warpMultiplier);
                    fragments[i].draw();
                }
            }

            if (scenePhase < 5) {
                animFrameId = requestAnimationFrame(renderLoop);
            }
        }

        // Start Master Timeline & Render Loop
        runMasterTimeline();
        renderLoop();
    }

})();
