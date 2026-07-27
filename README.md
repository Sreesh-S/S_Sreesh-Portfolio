# 🚀 S Sreesh — Developer Portfolio Website

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Live Website](https://img.shields.io/badge/Live--Demo-sreesh.pythonanywhere.com-00F5FF.svg?style=for-the-badge&logo=google-chrome&logoColor=black)](https://sreesh.pythonanywhere.com/)

A modern, ultra-premium developer portfolio web application built with **Django**, **Python**, **Vanilla CSS3**, **Three.js**, **GSAP**, **Typed.js**, and custom AI features. Designed for high performance, smooth interactive animations, real-time analytics, and seamless contact management.

🌐 **Live Website**: [https://sreesh.pythonanywhere.com/](https://sreesh.pythonanywhere.com/)

---

## 🌟 Key Features

- **🎨 Modern Dark & Light Theme**: Built with a custom futuristic design system, glassmorphism cards, glowing accent borders, and persistent theme memory.
- **⚡ GSAP & Lenis Smooth Animations**: Smooth inertia scrolling, dynamic letter reveals, and scroll-triggered section transitions.
- **🤖 Integrated Floating AI Assistant**: An interactive AI chatbot that answers visitor questions about projects, skills, education, and contact channels in real time.
- **📊 Developer Admin Analytics Dashboard**: A custom admin workspace featuring visitor IP geolocation tracking, country/city analytics, time-series charts, and contact message management.
- **💼 Interactive Project Showcase & Case Studies**: Project cards with multi-video 1.5x speed playback controls, tech stack badges, key capabilities, and direct links to source code repositories.
- **🔍 Command Palette (`Ctrl + K`)**: Instant search modal allowing visitors to search projects, skills, certifications, and blog articles instantly.
- **📄 Resume PDF Tracker & Downloader**: Tracks resume download analytics and serves the active resume PDF smoothly.
- **💬 WhatsApp Contact Forwarding**: Form submissions automatically format message text and redirect to WhatsApp (`+91 81294 10562`) while storing messages in the SQLite database.

---

## 🛠️ Tech Stack & Architecture

### Backend
- **Framework**: Django 5.0+ / Python 3.10+
- **Database**: SQLite3 (Local & Production persistent storage)
- **WSGI / Server**: Gunicorn & WhiteNoise (Compressed static asset handling)

### Frontend & UI
- **Core**: HTML5, Vanilla CSS3 (Custom Design System), JavaScript (ES6+)
- **3D & Canvas**: Three.js (Interactive 3D Mesh Particle Canvas)
- **Animations**: GSAP 3 (ScrollTrigger), Lenis Smooth Scroll, Typed.js
- **Icons & Typography**: FontAwesome 6, Google Fonts (Space Grotesk, Plus Jakarta Sans, Outfit, Fira Code)

---

## 📂 Project Structure

```
S_Sreesh-Portfolio/
├── manage.py
├── requirements.txt           # Production Dependencies (Django, gunicorn, whitenoise, Pillow)
├── Procfile                   # Process file for hosting platforms
├── build.sh                   # Automated deployment build script
├── .gitignore                 # Git ignore settings
│
├── portfolio/                 # Primary Django Application
│   ├── models.py              # Profile, Skill, Project, Experience, Visitor, ContactMessage models
│   ├── views.py               # View logic, AI assistant API, visitor analytics, resume handler
│   ├── urls.py                # App URL routing
│   ├── forms.py               # Contact message validation form
│   └── management/
│       └── commands/
│           └── seed_portfolio.py # Automated database seeder
│
├── portfolio_project/         # Django Settings & Core Configuration
│   ├── settings.py            # Environment, static/media storage, & security headers
│   ├── urls.py                # Root URL router & static/media handlers
│   └── wsgi.py                # WSGI entry point
│
├── templates/                 # HTML5 Templates
│   ├── base.html              # Core layout template with Open Graph SEO & AI widget
│   ├── home.html              # Main single-page portfolio layout
│   ├── projects.html          # Projects gallery page
│   ├── project_detail.html    # Detailed project case study view
│   ├── skills.html            # Skills breakdown view
│   ├── experience.html        # Work experience & education timeline
│   ├── certifications.html    # Verified certifications gallery
│   ├── contact.html           # Contact form page
│   └── admin_dashboard.html   # Custom developer analytics workspace
│
├── static/                    # Frontend Static Assets
│   ├── css/
│   │   ├── main.css           # Design system, CSS tokens, dark/light themes
│   │   └── intro-animation.css
│   ├── js/
│   │   ├── main.js            # GSAP animations, Lenis scroll, video controls
│   │   ├── ai_assistant.js    # AI chatbot widget logic
│   │   ├── command_palette.js # Fuzzy search modal logic
│   │   ├── intro-animation.js # Startup matrix code animation
│   │   └── three_bg.js        # Three.js 3D background canvas
│   └── images/
│       ├── profile.jpeg       # Static fallback profile photo
│       └── portfolio_banner.png # 1200x630 Open Graph LinkedIn preview banner
│
└── media/                     # Uploaded Media Files
    ├── profile/               # Main profile picture
    ├── profile images/        # About section slideshow photos
    ├── resumes/               # Resume PDF files
    └── [project folders]/     # Project preview MP4 video files
```

---

## ⚡ Quick Start & Local Development

### 1. Clone the Repository
```bash
git clone https://github.com/Sreesh-S/S_Sreesh-Portfolio.git
cd S_Sreesh-Portfolio
```

### 2. Create and Activate Virtual Environment
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Portfolio Data
```bash
python manage.py migrate
python manage.py seed_portfolio
```

### 5. Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser to view the portfolio live! Access the admin dashboard at `http://127.0.0.1:8000/admin-dashboard/`.

---

## ☁️ Production Deployment (PythonAnywhere)

1. Open **Bash Console** on PythonAnywhere:
   ```bash
   git clone https://github.com/Sreesh-S/S_Sreesh-Portfolio.git
   cd S_Sreesh-Portfolio
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_portfolio
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

2. Configure **Web Tab** on PythonAnywhere:
   - **Source code**: `/home/Sreesh/S_Sreesh-Portfolio`
   - **Working directory**: `/home/Sreesh/S_Sreesh-Portfolio`
   - **Virtualenv**: `/home/Sreesh/S_Sreesh-Portfolio/venv`
   - **Static Files**:
     - `/static/` &rarr; `/home/Sreesh/S_Sreesh-Portfolio/staticfiles`
     - `/media/` &rarr; `/home/Sreesh/S_Sreesh-Portfolio/media`

3. Click **Reload** to make your site live!

---

## 📬 Contact & Connect

- **Author**: S Sreesh
- **Location**: Kerala, India
- **Email**: [ssreesh45@gmail.com](mailto:ssreesh45@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/s-sreesh](https://www.linkedin.com/in/s-sreesh)
- **GitHub**: [https://github.com/Sreesh-S](https://github.com/Sreesh-S)
- **Live Portfolio**: [https://sreesh.pythonanywhere.com/](https://sreesh.pythonanywhere.com/)

---

*Designed and engineered by S Sreesh.*
