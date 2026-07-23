/* -------------------------------------------------------------
   CORE MAIN JAVASCRIPT (LENIS, GSAP, TYPED, FORM, CURSOR)
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Loader Closing Simulation
    const preloader = document.getElementById('preloader');
    let introTriggered = false;
    
    function triggerPreloaderHide() {
        if (introTriggered) return;
        introTriggered = true;
        if (preloader) {
            preloader.style.opacity = '0';
            preloader.style.transition = 'opacity 0.5s ease';
            setTimeout(() => {
                preloader.style.display = 'none';
                playIntroAnimations();
            }, 500);
        } else {
            playIntroAnimations();
        }
    }

    if (preloader) {
        if (document.readyState === 'complete') {
            setTimeout(triggerPreloaderHide, 800);
        } else {
            window.addEventListener('load', function() {
                setTimeout(triggerPreloaderHide, 800);
            });
            // Safety timeout: force hide preloader after 1.5s max if load event delayed
            setTimeout(triggerPreloaderHide, 1500);
        }
    } else {
        playIntroAnimations();
    }

    // 2. Custom Cursor Spring Follower
    const cursor = document.getElementById('custom-cursor');
    const cursorDot = document.getElementById('custom-cursor-dot');
    
    let mouseX = 0, mouseY = 0;
    let ballX = 0, ballY = 0;
    let speed = 0.15; // Easing speed

    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        // Instant dot positioning
        if (cursorDot) {
            cursorDot.style.left = mouseX + 'px';
            cursorDot.style.top = mouseY + 'px';
        }
    });

    function animateCursor() {
        // Easing calculations
        let distX = mouseX - ballX;
        let distY = mouseY - ballY;
        
        ballX += distX * speed;
        ballY += distY * speed;
        
        if (cursor) {
            cursor.style.left = ballX + 'px';
            cursor.style.top = ballY + 'px';
        }
        
        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Hover scales
    const interactiveElements = document.querySelectorAll('a, button, .glass-card, .skills-cat-btn');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            if (cursor) {
                cursor.style.width = '450px';
                cursor.style.height = '450px';
            }
        });
        el.addEventListener('mouseleave', () => {
            if (cursor) {
                cursor.style.width = '300px';
                cursor.style.height = '300px';
            }
        });
    });

    // 3. Lenis Smooth Scroll Setup
    const lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // standard easing
        direction: 'vertical',
        gestureDirection: 'vertical',
        smooth: true,
        mouseMultiplier: 1,
        smoothTouch: false,
        touchMultiplier: 2,
        infinite: false,
    });

    function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // Link scroll anchors to Lenis
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                lenis.scrollTo(target, { offset: -20 });
            }
        });
    });

    // 4. GSAP & ScrollTrigger bindings
    gsap.registerPlugin(ScrollTrigger);

    // Update Lenis on scroll
    lenis.on('scroll', ScrollTrigger.update);

    // Sync GSAP with Lenis
    gsap.ticker.add((time) => {
        lenis.raf(time * 1000);
    });

    // Navbar Scrolled Backdrop State
    const navWrapper = document.querySelector('.navbar-wrapper');
    if (navWrapper) {
        ScrollTrigger.create({
            start: 'top -20',
            end: 99999,
            onToggle: self => {
                if (self.isActive) {
                    navWrapper.classList.add('scrolled');
                } else {
                    navWrapper.classList.remove('scrolled');
                }
            }
        });
    }

    // Scroll Progress bar
    const indicator = document.getElementById('scroll-indicator');
    if (indicator) {
        gsap.to(indicator, {
            width: '100%',
            ease: 'none',
            scrollTrigger: {
                trigger: 'body',
                start: 'top top',
                end: 'bottom bottom',
                scrub: true
            }
        });
    }

    // Dynamic Reveals
    function playIntroAnimations() {
        // Hero title letters reveal
        const letterDiv = document.getElementById('letter-reveal');
        if (letterDiv) {
            const rawText = letterDiv.getAttribute('data-text') || letterDiv.innerText || 'S Sreesh';
            letterDiv.innerHTML = '';
            // Wrap each letter in a span
            [...rawText].forEach(char => {
                const span = document.createElement('span');
                span.innerText = char === ' ' ? '\u00A0' : char;
                span.style.display = 'inline-block';
                span.style.opacity = '1';
                span.style.color = 'var(--primary-accent)';
                span.style.webkitTextFillColor = 'var(--primary-accent)';
                letterDiv.appendChild(span);
            });

            if (typeof gsap !== 'undefined') {
                gsap.from('#letter-reveal span', {
                    opacity: 0,
                    y: 15,
                    stagger: 0.04,
                    duration: 0.6,
                    ease: 'power2.out'
                });
            }
        }

        gsap.from('.reveal-text', { opacity: 0, y: 15, duration: 1, ease: 'power2.out' });
        gsap.from('.reveal-text-delay', { opacity: 0, y: 15, duration: 1, delay: 0.3, ease: 'power2.out' });
        gsap.from('.reveal-ctas', { opacity: 0, y: 20, duration: 1, delay: 0.5, ease: 'power2.out' });
        gsap.from('.hero-visual-content', { opacity: 0, scale: 0.9, duration: 1.2, delay: 0.2, ease: 'power3.out' });
        
        if (typeof ScrollTrigger !== 'undefined') {
            ScrollTrigger.refresh();
        }
    }
    window.playIntroAnimations = playIntroAnimations;

    // Robust Fail-Safe: Ensures all page content becomes visible even if GSAP/ScrollTrigger is delayed
    function forceShowScrollReveals() {
        const revealElems = document.querySelectorAll('.scroll-reveal-up, .scroll-reveal-left, .scroll-reveal-right, .reveal-text, .reveal-text-delay, .reveal-ctas');
        revealElems.forEach(elem => {
            const rect = elem.getBoundingClientRect();
            // If element is inside or near viewport (or user has scrolled past)
            if (rect.top < window.innerHeight + 150) {
                elem.style.opacity = '1';
                elem.style.visibility = 'visible';
                elem.style.transform = 'none';
            }
        });
    }

    // Scroll trigger reveals for each section with visibility callbacks
    gsap.utils.toArray('.scroll-reveal-up').forEach(elem => {
        gsap.from(elem, {
            opacity: 0,
            y: 30,
            duration: 0.8,
            scrollTrigger: {
                trigger: elem,
                start: 'top 92%',
                toggleActions: 'play none none none',
                onEnter: () => {
                    elem.style.opacity = '1';
                    elem.style.visibility = 'visible';
                }
            }
        });
    });

    gsap.utils.toArray('.scroll-reveal-left').forEach(elem => {
        gsap.from(elem, {
            opacity: 0,
            x: -30,
            duration: 0.8,
            scrollTrigger: {
                trigger: elem,
                start: 'top 92%',
                toggleActions: 'play none none none',
                onEnter: () => {
                    elem.style.opacity = '1';
                    elem.style.visibility = 'visible';
                }
            }
        });
    });

    gsap.utils.toArray('.scroll-reveal-right').forEach(elem => {
        gsap.from(elem, {
            opacity: 0,
            x: 30,
            duration: 0.8,
            scrollTrigger: {
                trigger: elem,
                start: 'top 92%',
                toggleActions: 'play none none none',
                onEnter: () => {
                    elem.style.opacity = '1';
                    elem.style.visibility = 'visible';
                }
            }
        });
    });

    // Run fail-safe reveal checks on scroll and after timers
    window.addEventListener('scroll', forceShowScrollReveals, { passive: true });
    setTimeout(forceShowScrollReveals, 1000);
    setTimeout(forceShowScrollReveals, 2500);
    setTimeout(() => {
        // Ultimate fallback: ensure ALL elements are 100% visible after 3.5s
        document.querySelectorAll('.scroll-reveal-up, .scroll-reveal-left, .scroll-reveal-right, .reveal-text, .reveal-text-delay, .reveal-ctas').forEach(el => {
            el.style.opacity = '1';
            el.style.visibility = 'visible';
            el.style.transform = 'none';
        });
    }, 3500);

    // 5. Typed.js Subtitle typing
    const typedSubtitle = document.getElementById('typed-subtitle');
    if (typedSubtitle) {
        new Typed('#typed-subtitle', {
            strings: [
                'Software Developer',
                'Python Specialist',
                'Software Tester',
                'Machine Learning Enthusiast',
                'Cyber Security Enthusiast',
                'Data Science and Data Analytics Enthusiast'
            ],
            typeSpeed: 50,
            backSpeed: 30,
            backDelay: 2000,
            loop: true,
            showCursor: true,
            cursorChar: '|'
        });
    }

    // Typing inside terminal section mockup
    const termTyping = document.getElementById('terminal-typing-text');
    if (termTyping) {
        new Typed('#terminal-typing-text', {
            strings: ['cat config.json', 'python init_portfolio.py'],
            typeSpeed: 60,
            backSpeed: 40,
            backDelay: 1500,
            loop: false,
            onComplete: function() {
                const out = document.getElementById('terminal-output');
                if (out) out.classList.remove('hidden');
            }
        });
    }

    // 6. Magnetic Buttons micro-interaction
    const magneticBtns = document.querySelectorAll('.magnetic');
    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', function(e) {
            const position = this.getBoundingClientRect();
            const x = e.clientX - position.left - (position.width / 2);
            const y = e.clientY - position.top - (position.height / 2);
            
            // Move button slightly towards mouse
            this.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translate(0px, 0px)';
        });
    });

    // 7. Light/Dark theme switcher
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        // Check localstorage
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme === 'light') {
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
        }

        themeBtn.addEventListener('click', function() {
            if (document.body.classList.contains('dark-theme')) {
                document.body.classList.remove('dark-theme');
                document.body.classList.add('light-theme');
                localStorage.setItem('theme', 'light');
            } else {
                document.body.classList.remove('light-theme');
                document.body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark');
            }
        });
    }

    // 8. Mobile navigation toggle
    const mobileToggle = document.getElementById('mobile-toggle');
    const navMenu = document.getElementById('nav-menu');
    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('open');
            // Toggle hamburger icon between bars and times
            const icon = mobileToggle.querySelector('i');
            if (navMenu.classList.contains('open')) {
                icon.className = 'fa-solid fa-xmark';
            } else {
                icon.className = 'fa-solid fa-bars-staggered';
            }
        });

        // Close when clicking nav items
        navMenu.querySelectorAll('a').forEach(item => {
            item.addEventListener('click', () => {
                navMenu.classList.remove('open');
                mobileToggle.querySelector('i').className = 'fa-solid fa-bars-staggered';
            });
        });
    }

    // 9. Skills section filtering tabs & progress loading
    const catBtns = document.querySelectorAll('.skills-cat-btn');
    const skillCards = document.querySelectorAll('.skill-card');
    
    // Function to animate skill progress fills
    function animateSkillsProgress() {
        skillCards.forEach(card => {
            const fill = card.querySelector('.skill-progress-bar-fill');
            if (fill && card.style.display !== 'none') {
                const targetLevel = fill.getAttribute('data-level');
                fill.style.width = targetLevel + '%';
            }
        });
    }

    if (catBtns.length > 0) {
        catBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Toggle active state
                catBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const category = this.getAttribute('data-category');
                
                skillCards.forEach(card => {
                    const cardCat = card.getAttribute('data-skill-cat');
                    if (category === 'all' || cardCat === category) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
                
                // Triggers progress fills
                setTimeout(animateSkillsProgress, 50);
            });
        });

        // Animate on scroll trigger
        ScrollTrigger.create({
            trigger: '.skills-section',
            start: 'top 75%',
            onEnter: () => animateSkillsProgress()
        });
    }

    // 10. AJAX contact form submission
    const contactForm = document.getElementById('portfolio-contact-form');
    const formLoader = document.getElementById('form-loader');
    const formSuccess = document.getElementById('form-success');
    const resetBtn = document.getElementById('reset-form-btn');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Clear previous errors
            document.querySelectorAll('.field-error-msg').forEach(el => el.innerText = '');

            // Show loader overlay
            if (formLoader) formLoader.classList.remove('hidden');

            const formData = new FormData(this);

            fetch(this.getAttribute('action'), {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: formData
            })
            .then(res => {
                if (formLoader) formLoader.classList.add('hidden');
                
                if (res.ok) {
                    return res.json().then(data => {
                        if (data.status === 'success') {
                            // Extract details for WhatsApp redirection
                            const name = formData.get('name');
                            const email = formData.get('email');
                            const phone = formData.get('phone') || 'N/A';
                            const message = formData.get('message');
                            
                            // Format the WhatsApp message text
                            const waText = `Hi Sreesh,\n\nI just sent a message from your portfolio website:\n\n*Name:* ${name}\n*Email:* ${email}\n*Phone:* ${phone}\n*Message:* ${message}`;
                            const waUrl = `https://wa.me/918129410562?text=${encodeURIComponent(waText)}`;
                            
                            // Open WhatsApp message draft in a new tab
                            window.open(waUrl, '_blank');
                            
                            if (formSuccess) formSuccess.classList.remove('hidden');
                            contactForm.reset();
                        }
                    });
                } else {
                    return res.json().then(data => {
                        // Display field validations
                        if (data.errors) {
                            for (const [field, errors] of Object.entries(data.errors)) {
                                const errorContainer = document.getElementById(`error-${field}`);
                                if (errorContainer && errors.length > 0) {
                                    errorContainer.innerText = errors[0].message;
                                }
                            }
                        }
                    });
                }
            })
            .catch(err => {
                if (formLoader) formLoader.classList.add('hidden');
                alert("Something went wrong. Please check your connection and try again.");
                console.error(err);
            });
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (formSuccess) formSuccess.classList.add('hidden');
        });
    }

    // 11. Count-up statistics logic
    const countElements = document.querySelectorAll('.count-up');
    if (countElements.length > 0) {
        ScrollTrigger.create({
            trigger: '.stats-container',
            start: 'top 85%',
            onEnter: () => {
                countElements.forEach(el => {
                    const target = parseInt(el.getAttribute('data-target'));
                    const duration = 1.5; // seconds
                    let current = 0;
                    const step = Math.ceil(target / (duration * 60)); // 60 FPS
                    
                    const timer = setInterval(() => {
                        current += step;
                        if (current >= target) {
                            el.innerText = target;
                            clearInterval(timer);
                        } else {
                            el.innerText = current;
                        }
                    }, 1000 / 60);
                });
            }
        });
    }

    // 12. Resume Analytics Click Tracker
    const resumeLinks = document.querySelectorAll('.cv-download-tracker, .cv-btn');
    resumeLinks.forEach(link => {
        link.addEventListener('click', function() {
            console.log("Resume download triggered and tracked.");
        });
    });

    // 13. Profile Photo Slideshow Carousel
    const frames = document.querySelectorAll('.about-img-frame');
    frames.forEach(frame => {
        const images = frame.querySelectorAll('.profile-slideshow-img');
        if (images.length > 1) {
            let currentIndex = 0;
            setInterval(() => {
                // Fade out current image
                images[currentIndex].style.opacity = '0';
                images[currentIndex].classList.remove('active');
                
                // Advance to next image
                currentIndex = (currentIndex + 1) % images.length;
                
                // Fade in next image
                images[currentIndex].style.opacity = '1';
                images[currentIndex].classList.add('active');
            }, 3000); // 3 seconds interval
        }
    });

    // 14. Featured Project Video Player Controller
    const featuredVideo = document.getElementById('featured-video');
    if (featuredVideo) {
        // Set speed to 1.5x
        featuredVideo.playbackRate = 1.5;
        
        const playBtn = document.getElementById('video-play-btn');
        const muteBtn = document.getElementById('video-mute-btn');
        const timeline = document.getElementById('video-timeline');
        const timeCurrent = document.getElementById('video-time-current');
        const timeTotal = document.getElementById('video-time-total');
        
        // Play / Pause toggle
        playBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (featuredVideo.paused) {
                featuredVideo.play();
                playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
            } else {
                featuredVideo.pause();
                playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
            }
        });

        // Mute / Unmute toggle
        muteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (featuredVideo.muted) {
                featuredVideo.muted = false;
                muteBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
            } else {
                featuredVideo.muted = true;
                muteBtn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
            }
        });

        // Update timeline as video plays
        featuredVideo.addEventListener('timeupdate', () => {
            if (!isNaN(featuredVideo.duration)) {
                const percentage = (featuredVideo.currentTime / featuredVideo.duration) * 100;
                timeline.value = percentage;
                
                // Format time helper
                const formatTime = (time) => {
                    const mins = Math.floor(time / 60);
                    const secs = Math.floor(time % 60);
                    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
                };
                timeCurrent.innerText = formatTime(featuredVideo.currentTime);
                timeTotal.innerText = formatTime(featuredVideo.duration);
            }
        });

        // Seek video on input dragging
        timeline.addEventListener('input', () => {
            if (!isNaN(featuredVideo.duration)) {
                const time = (timeline.value / 100) * featuredVideo.duration;
                featuredVideo.currentTime = time;
            }
        });
    }

    // 15. Universal Project Video Player Controller
    const videoWrappers = document.querySelectorAll('.project-video-wrapper');
    videoWrappers.forEach(wrapper => {
        const slug = wrapper.dataset.projectSlug;
        const video = wrapper.querySelector('.project-preview-video');
        const playBtn = wrapper.querySelector('.video-play-btn');
        const muteBtn = wrapper.querySelector('.video-mute-btn');
        const scrubber = wrapper.querySelector('.video-timeline-scrubber');
        const controls = wrapper.querySelector('.project-video-controls');
        const counterBadge = wrapper.querySelector('.video-counter-badge');

        const prevBtns = wrapper.querySelectorAll('.video-prev-btn, .video-prev-btn-bar');
        const nextBtns = wrapper.querySelectorAll('.video-next-btn, .video-next-btn-bar');

        if (!video) return;

        // Try to get multi-video list from data-videos attribute or json script tag
        let videoList = [];
        const rawVideos = wrapper.dataset.videos;
        if (rawVideos) {
            try {
                videoList = JSON.parse(rawVideos);
            } catch (e) {
                console.error("Error parsing data-videos for " + slug, e);
            }
        }
        if (!videoList || videoList.length === 0) {
            const dataScript = document.getElementById(`${slug}-videos-data`);
            if (dataScript) {
                try {
                    videoList = JSON.parse(dataScript.textContent);
                } catch (e) {
                    console.error("Error parsing video data for " + slug, e);
                }
            }
        }

        let currentIdx = 0;

        function loadVideoIndex(idx) {
            if (!videoList || videoList.length === 0) return;
            currentIdx = (idx + videoList.length) % videoList.length;
            video.src = videoList[currentIdx];
            video.load();
            video.playbackRate = 1.5;
            const playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.catch(e => console.log("Video play error: ", e));
            }

            if (playBtn) playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';

            if (counterBadge) {
                counterBadge.innerText = `${currentIdx + 1}/${videoList.length} • 1.5x Speed`;
            }
        }

        // Default 1.5x Speed
        video.playbackRate = 1.5;
        video.addEventListener('play', () => {
            video.playbackRate = 1.5;
        });

        // Multi-video playlist handler
        if (videoList && videoList.length > 1) {
            video.loop = false;
            video.addEventListener('ended', () => {
                loadVideoIndex(currentIdx + 1);
            });

            prevBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    e.preventDefault();
                    loadVideoIndex(currentIdx - 1);
                });
            });

            nextBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    e.preventDefault();
                    loadVideoIndex(currentIdx + 1);
                });
            });
        } else {
            video.loop = true;
        }

        // Hover controls visibility
        if (controls) {
            const hoverContainer = wrapper.closest('.project-card') || wrapper.closest('.detail-card') || wrapper.closest('.featured-project-card') || wrapper;
            hoverContainer.addEventListener('mouseenter', () => {
                controls.style.opacity = '1';
                prevBtns.forEach(b => b.style.opacity = '1');
                nextBtns.forEach(b => b.style.opacity = '1');
            });
            hoverContainer.addEventListener('mouseleave', () => {
                controls.style.opacity = '0';
                prevBtns.forEach(b => b.style.opacity = '0.8');
                nextBtns.forEach(b => b.style.opacity = '0.8');
            });
        }

        // Play / Pause toggle
        if (playBtn) {
            playBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (video.paused) {
                    video.play();
                    playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
                } else {
                    video.pause();
                    playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
                }
            });
        }

        // Mute / Unmute toggle
        if (muteBtn) {
            muteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (video.muted) {
                    video.muted = false;
                    muteBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
                } else {
                    video.muted = true;
                    muteBtn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
                }
            });
        }

        // Scrubber update & dragging
        if (scrubber) {
            video.addEventListener('timeupdate', () => {
                if (!isNaN(video.duration) && video.duration > 0) {
                    scrubber.value = (video.currentTime / video.duration) * 100;
                }
            });
            scrubber.addEventListener('input', (e) => {
                e.stopPropagation();
                if (!isNaN(video.duration) && video.duration > 0) {
                    video.currentTime = (scrubber.value / 100) * video.duration;
                }
            });
        }
    });
});
