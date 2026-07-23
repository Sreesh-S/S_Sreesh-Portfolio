from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, FileResponse, Http404
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
import json
import urllib.request
import os

from .models import (
    Profile, Skill, Project, Experience, Education, 
    Certification, ContactMessage, Visitor, ResumeAnalytics, Blog, SocialLinks, ResumeFile
)
from .forms import ContactMessageForm

def track_visitor(request):
    """Logs unique visitor visits based on IP address and tries to resolve location."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Avoid duplicate logging within 15 minutes for the same IP
    recent_visit = Visitor.objects.filter(
        ip_address=ip, 
        visit_time__gte=timezone.now() - timedelta(minutes=15)
    ).exists()
    
    if recent_visit:
        return

    country = "Unknown"
    city = "Unknown"
    
    if ip not in ['127.0.0.1', 'localhost', '::1']:
        try:
            url = f"http://ip-api.com/json/{ip}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=1.5) as response:
                data = json.loads(response.read().decode())
                if data.get('status') == 'success':
                    country = data.get('country', 'Unknown')
                    city = data.get('city', 'Unknown')
        except Exception:
            pass

    Visitor.objects.create(ip_address=ip, country=country, city=city)


import urllib.parse

def get_profile_images():
    """Helper to retrieve all uploaded files inside media/profile images directory."""
    img_dir = os.path.join(settings.MEDIA_ROOT, 'profile images')
    images = []
    if os.path.exists(img_dir):
        try:
            files = os.listdir(img_dir)
            for f in sorted(files):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
                    encoded_f = urllib.parse.quote(f)
                    images.append(f'/media/profile%20images/{encoded_f}')
        except Exception:
            pass
    if not images:
        images.append('/static/images/profile.jpeg')
    return images


def get_main_profile_pic():
    """Helper to retrieve the single uploaded profile photo inside media/profile directory."""
    img_dir = os.path.join(settings.MEDIA_ROOT, 'profile')
    if os.path.exists(img_dir):
        try:
            files = os.listdir(img_dir)
            for f in sorted(files):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
                    encoded_f = urllib.parse.quote(f)
                    return f'/media/profile/{encoded_f}'
        except Exception:
            pass
    return '/static/images/profile.jpeg'


def get_health_app_videos():
    """Helper to retrieve all uploaded files inside media/health app preview directory."""
    video_dir = os.path.join(settings.MEDIA_ROOT, 'health app preview')
    if not os.path.exists(video_dir):
        return []
    try:
        files = os.listdir(video_dir)
        videos = []
        for f in sorted(files):
            if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                videos.append(f'/media/health app preview/{f}')
        return videos
    except Exception:
        return []


def get_project_preview_videos(project):
    """Helper to retrieve all uploaded preview video files for a specific project."""
    title_lower = project.title.lower()
    
    mapping = [
        (('dos', 'ddos'), 'doss preview'),
        (('blood', 'health', 'analyzer', 'disease', 'report'), 'health app preview'),
        (('ev charging', 'charge'), 'Chargequest preview'),
        (('vkart', 'vcart', 'grocery'), 'vcart preview'),
        (('draupadi', 'draupathi', 'saree'), 'Draupathi preview'),
    ]
    
    target_folder = None
    for keywords, folder in mapping:
        if any(kw in title_lower for kw in keywords):
            target_folder = folder
            break
            
    if not target_folder:
        return []
        
    video_dir = os.path.join(settings.MEDIA_ROOT, target_folder)
    if not os.path.exists(video_dir):
        return []
        
    try:
        files = os.listdir(video_dir)
        videos = []
        for f in sorted(files):
            if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                videos.append(f'/media/{target_folder}/{f}')
        return videos
    except Exception:
        return []


def home(request):
    """Renders the single page portfolio layout with all key sections."""
    track_visitor(request)
    
    # Get S Sreesh's profile (create default if not exists)
    profile = Profile.objects.first()
    if not profile:
        profile = Profile.objects.create(
            name="S Sreesh",
            title="Software Developer | Python Developer",
            location="Kerala, India",
            email="ssreesh45@gmail.com",
            bio="Passionate Software Developer and Python enthusiast with expertise in Django, Machine Learning, Cyber Security, and Data Analytics. Committed to crafting high-performance, dynamic applications and solving complex architectural challenges."
        )
    
    skills = Skill.objects.all()
    projects = Project.objects.all().order_by('-is_featured', 'id')
    for p in projects:
        p.preview_videos = get_project_preview_videos(p)
        p.preview_videos_json = json.dumps(p.preview_videos)

    experiences = Experience.objects.all()
    educations = Education.objects.all()
    certifications = Certification.objects.all()
    blogs = Blog.objects.all()[:3]
    socials = SocialLinks.objects.all()
    
    # Contact form
    form = ContactMessageForm()
    
    # Stats counts
    stats = {
        'projects_count': Project.objects.count(),
        'experience_years': 1, # e.g. internship and freelance
        'skills_count': Skill.objects.count(),
        'certifications_count': Certification.objects.count(),
        'visitors_count': Visitor.objects.count()
    }
    
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'educations': educations,
        'certifications': certifications,
        'blogs': blogs,
        'socials': socials,
        'form': form,
        'stats': stats,
        'profile_images': get_profile_images(),
        'main_profile_pic': get_main_profile_pic(),
        'health_videos': get_health_app_videos(),
    }
    return render(request, 'home.html', context)


def about(request):
    """Individual About page view."""
    profile = Profile.objects.first()
    educations = Education.objects.all()
    stats = {
        'projects_count': Project.objects.count(),
        'skills_count': Skill.objects.count(),
        'certifications_count': Certification.objects.count()
    }
    return render(request, 'about.html', {
        'profile': profile, 
        'educations': educations,
        'stats': stats,
        'profile_images': get_profile_images(),
    })


def projects(request):
    """Individual Projects listing page view."""
    projects = Project.objects.all().order_by('-is_featured', 'id')
    for p in projects:
        p.preview_videos = get_project_preview_videos(p)
        p.preview_videos_json = json.dumps(p.preview_videos)
    return render(request, 'projects.html', {'projects': projects})


def project_detail(request, slug):
    """Detailed Case Study view for a specific project."""
    project = get_object_or_404(Project, slug=slug)
    project.preview_videos = get_project_preview_videos(project)
    project.preview_videos_json = json.dumps(project.preview_videos)
    # Get related projects excluding current one
    related_projects = Project.objects.exclude(id=project.id)[:3]
    for rp in related_projects:
        rp.preview_videos = get_project_preview_videos(rp)
        rp.preview_videos_json = json.dumps(rp.preview_videos)
    return render(request, 'project_detail.html', {
        'project': project,
        'related_projects': related_projects
    })


def skills(request):
    """Individual Skills category grid view."""
    skills = Skill.objects.all()
    # Group skills by categories
    categories = {}
    for s in skills:
        categories.setdefault(s.get_category_display(), []).append(s)
    return render(request, 'skills.html', {'categories': categories})


def experience(request):
    """Individual Timeline experience & education view."""
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    return render(request, 'experience.html', {
        'experiences': experiences,
        'educations': educations
    })


def certifications(request):
    """Individual Certifications gallery view."""
    certifications = Certification.objects.all()
    return render(request, 'certifications.html', {'certifications': certifications})


def contact(request):
    """Asynchronous contact message handling with validation and notifications."""
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message_obj = form.save()
            
            # Send Email Notification to S Sreesh
            try:
                subject = f"Portfolio Alert: Message from {message_obj.name}"
                body = (
                    f"You received a new message on your portfolio:\n\n"
                    f"Name: {message_obj.name}\n"
                    f"Email: {message_obj.email}\n"
                    f"Phone: {message_obj.phone or 'N/A'}\n"
                    f"Message:\n{message_obj.message}\n\n"
                    f"View details at your custom dashboard."
                )
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True
                )
            except Exception:
                pass
                
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you! Your message has been sent successfully. Sreesh will get in touch shortly.'
                })
            return redirect('portfolio:home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors.get_json_data()
                }, status=400)
    else:
        form = ContactMessageForm()
        
    return render(request, 'contact.html', {'form': form})


def download_resume(request):
    """Serves the active resume PDF and tracks the action in download analytics."""
    # Track the download IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')
    try:
        ResumeAnalytics.objects.create(ip_address=ip)
    except Exception:
        pass

    # 1. Check for explicitly active ResumeFile
    active_resume = ResumeFile.objects.filter(is_active=True).first()
    if active_resume and active_resume.file:
        try:
            return FileResponse(active_resume.file.open('rb'), as_attachment=True, filename="S_Sreesh_Resume.pdf")
        except Exception:
            pass
    
    # 2. Fallback to Profile resume field
    profile = Profile.objects.first()
    if profile and profile.resume:
        try:
            return FileResponse(profile.resume.open('rb'), as_attachment=True, filename="S_Sreesh_Resume.pdf")
        except Exception:
            pass
            
    # 3. Direct File Fallback to media/resumes/sreesh_resume.pdf
    resume_path = os.path.join(settings.MEDIA_ROOT, 'resumes', 'sreesh_resume.pdf')
    if os.path.exists(resume_path):
        return FileResponse(open(resume_path, 'rb'), as_attachment=True, filename="S_Sreesh_Resume.pdf")
    
    raise Http404("Resume file not found. Please upload it via the Django admin.")



def blog_list(request):
    """Renders blog post entries."""
    blogs = Blog.objects.all()
    return render(request, 'blog.html', {'blogs': blogs})


def blog_detail(request, slug):
    """Renders details of a blog article."""
    blog = get_object_or_404(Blog, slug=slug)
    related_blogs = Blog.objects.exclude(id=blog.id)[:3]
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'related_blogs': related_blogs
    })


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def admin_dashboard(request):
    """A beautiful, premium custom admin workspace for visitor analytics and portfolio management."""
    messages = ContactMessage.objects.all()
    unread_count = ContactMessage.objects.filter(is_read=False).count()
    
    # Visitor stats
    visitors_by_country = Visitor.objects.values('country').annotate(count=Count('country')).order_by('-count')
    visitors_by_city = Visitor.objects.values('city', 'country').annotate(count=Count('city')).order_by('-count')[:10]
    total_visits = Visitor.objects.count()
    
    # Time-series visitor charts (last 7 days)
    last_7_days = []
    visitor_trend = []
    today = timezone.now().date()
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        last_7_days.append(day.strftime("%b %d"))
        visitor_trend.append(Visitor.objects.filter(visit_time__date=day).count())
        
    # Resume download count
    total_downloads = ResumeAnalytics.objects.count()
    
    profile = Profile.objects.first()
    profile_resume_url = profile.resume.url if (profile and profile.resume) else None
    
    # Auto-sync legacy profile resume to ResumeFile table if empty
    if ResumeFile.objects.count() == 0 and profile and profile.resume:
        ResumeFile.objects.create(
            title=os.path.basename(profile.resume.name),
            file=profile.resume,
            is_active=True
        )
    
    resumes = ResumeFile.objects.all()
    active_resume = ResumeFile.objects.filter(is_active=True).first()
    if not active_resume and resumes.exists():
        active_resume = resumes.first()
        active_resume.is_active = True
        active_resume.save()
    
    # About Section & Profile Pictures
    about_photos = get_profile_images()
    about_photo_names = [os.path.basename(p) for p in about_photos]
    
    context = {
        'messages': messages,
        'unread_count': unread_count,
        'visitors_by_country': list(visitors_by_country),
        'visitors_by_city': list(visitors_by_city),
        'total_visits': total_visits,
        'total_downloads': total_downloads,
        'last_7_days': last_7_days,
        'visitor_trend': visitor_trend,
        'projects': Project.objects.all().order_by('-is_featured', 'id'),
        'skills': Skill.objects.all(),
        'certifications': Certification.objects.all(),
        'experiences': Experience.objects.all(),
        'resumes': resumes,
        'active_resume': active_resume,
        'profile': profile,
        'profile_resume_url': profile_resume_url or (active_resume.file.url if active_resume and active_resume.file else None),
        'main_profile_pic': get_main_profile_pic(),
        'about_photos': about_photos,
        'about_photo_names': about_photo_names,
    }
    return render(request, 'admin_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def toggle_message_read(request, message_id):
    """Toggles read status of contact message."""
    msg = get_object_or_404(ContactMessage, id=message_id)
    msg.is_read = not msg.is_read
    msg.save()
    return JsonResponse({'status': 'success', 'is_read': msg.is_read})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_message(request, message_id):
    """Deletes a contact message."""
    msg = get_object_or_404(ContactMessage, id=message_id)
    msg.delete()
    return JsonResponse({'status': 'success'})


def command_palette_search(request):
    """API search endpoint matching query against projects, skills, certificates and blogs."""
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        # Search Projects
        projects = Project.objects.filter(
            Q(title__icontains=query) | 
            Q(tech_stack__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        for p in projects:
            results.append({
                'title': p.title,
                'category': 'Project',
                'url': f"/project/{p.slug}/",
                'subtitle': p.subtitle or p.tech_stack
            })
            
        # Search Skills
        skills = Skill.objects.filter(name__icontains=query)[:5]
        for s in skills:
            results.append({
                'title': s.name,
                'category': 'Skill',
                'url': '/skills/',
                'subtitle': s.category
            })
            
        # Search Certifications
        certs = Certification.objects.filter(name__icontains=query)[:5]
        for c in certs:
            results.append({
                'title': c.name,
                'category': 'Certification',
                'url': '/certifications/',
                'subtitle': c.issuing_organization
            })
            
        # Search Blogs
        blogs = Blog.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        )[:5]
        for b in blogs:
            results.append({
                'title': b.title,
                'category': 'Blog',
                'url': f"/blog/{b.slug}/",
                'subtitle': f"{b.read_time} min read"
            })
            
    return JsonResponse({'results': results})


def ai_assistant(request):
    """Asynchronous AI floating assistant. Simulates FAQ responses based on keywords."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_msg = data.get('message', '').lower().strip()
        except Exception:
            user_msg = request.POST.get('message', '').lower().strip()
            
        if not user_msg:
            return JsonResponse({'reply': "Hi there! I am Sreesh's custom AI Assistant. Ask me anything!"})
            
        reply = ""
        # Match keywords
        if any(w in user_msg for w in ['hello', 'hi', 'hey', 'greetings']):
            reply = "Hello! I am Sreesh's AI Assistant. I can tell you about his projects, skills, education, experience, or certifications. Ask me anything!"
        elif any(w in user_msg for w in ['project', 'portfolio', 'work']):
            reply = (
                "Sreesh has built several impressive applications:<br>"
                "• <strong>DoS/DDoS Attack Detection System</strong> (Featured Cyber Security ML app)<br>"
                "• <strong>Smart Blood Report Analyzer</strong> (Medical OCR & AI Analyzer)<br>"
                "• <strong>EV Charging Station Locator</strong> (Node.js Station Map)<br>"
                "• <strong>VKART Grocery Website</strong> (Full E-Commerce Web App)<br><br>"
                "Ask me about any project title (e.g. 'blood report') to learn more!"
            )
        elif any(w in user_msg for w in ['ddos', 'dos', 'attack', 'detection']):
            reply = (
                "The <strong>Machine Learning Based DoS/DDoS Attack Detection System</strong> is Sreesh's featured project. "
                "It uses the CICIDS2017 dataset to train a Random Forest model, detecting security attacks in real time. "
                "It logs threats, shows live charts in an interactive dashboard, and was built using Python, Django, and Scikit-learn."
            )
        elif any(w in user_msg for w in ['blood', 'report', 'analyzer', 'ocr']):
            reply = (
                "The <strong>Smart Blood Report Analyzer</strong> uses Optical Character Recognition (OCR) to parse PDF medical lab reports, "
                "extract blood metrics, compare them against reference values, and predict potential diseases using Python AI libraries."
            )
        elif any(w in user_msg for w in ['ev', 'charging', 'station', 'locator']):
            reply = (
                "The <strong>EV Charging Station Locator</strong> is a node-based platform that displays charging station networks, "
                "availability status, and locations on interactive map components."
            )
        elif any(w in user_msg for w in ['vkart', 'grocery', 'ecommerce']):
            reply = (
                "<strong>VKART</strong> is a dynamic grocery shopping application supporting full user carts, simulated checkout orders, "
                "home delivery indicators, and admin catalog management."
            )
        elif any(w in user_msg for w in ['skill', 'tech', 'language', 'stack']):
            reply = (
                "Here is Sreesh's toolkit:<br>"
                "• <strong>Programming</strong>: Python, Java, C, PHP<br>"
                "• <strong>Web Dev</strong>: HTML5, CSS3, JavaScript, Django, Node.js<br>"
                "• <strong>Machine Learning</strong>: Scikit-learn, Pandas, NumPy<br>"
                "• <strong>Databases</strong>: MySQL, MongoDB<br>"
                "• <strong>Tools</strong>: Git, GitHub, VS Code, Power BI"
            )
        elif any(w in user_msg for w in ['contact', 'email', 'phone', 'number', 'mobile', 'call', 'whatsapp', 'reach', 'social', 'linkedin']):
            profile = Profile.objects.first()
            phone_num = profile.phone if profile else "+91 81294 10562"
            email_addr = profile.email if profile else "ssreesh45@gmail.com"
            reply = (
                "You can reach S Sreesh directly via:<br>"
                f"• <strong>Phone / WhatsApp</strong>: <a href='https://wa.me/918129410562' target='_blank' class='accent-text'>{phone_num}</a><br>"
                f"• <strong>Email</strong>: <a href='mailto:{email_addr}' class='accent-text'>{email_addr}</a><br>"
                "• <strong>LinkedIn</strong>: <a href='https://www.linkedin.com/in/s-sreesh' target='_blank' class='accent-text'>s-sreesh</a><br>"
                "• <strong>GitHub</strong>: <a href='https://github.com/Sreesh-S' target='_blank' class='accent-text'>Sreesh-S</a><br><br>"
                "Alternatively, write a message in the contact form at the bottom of the page!"
            )
        elif any(w in user_msg for w in ['education', 'college', 'mca', 'bca']):
            reply = "Sreesh holds a Master of Computer Applications (MCA) and a Bachelor of Computer Applications (BCA) from Kerala, India."
        elif any(w in user_msg for w in ['experience', 'intern', 'job', 'alpha']):
            reply = (
                "Sreesh completed a <strong>Cyber Security Internship</strong> at <strong>Alpha Innovation</strong> (June 2024 - August 2024). "
                "His work involved analyzing vulnerabilities, monitoring network logs, and simulating penetration testing."
            )
        elif any(w in user_msg for w in ['cert', 'certification', 'course']):
            reply = (
                "Sreesh holds professional certifications in Python, Machine Learning, and Cyber Security. "
                "Scroll down to the Certifications section to see his verified credentials and links!"
            )
        else:
            reply = (
                "I'm not fully sure about that, but feel free to check out Sreesh's resume or "
                "drop him a quick note at <a href='mailto:ssreesh45@gmail.com'>ssreesh45@gmail.com</a>!"
            )
            
        return JsonResponse({'reply': reply})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def sitemap_view(request):
    """Generates sitemap.xml dynamically."""
    projects = Project.objects.all()
    blogs = Blog.objects.all()
    return render(request, 'sitemap.xml', {
        'projects': projects, 
        'blogs': blogs,
        'today': timezone.now().date().isoformat()
    }, content_type="application/xml")


def robots_view(request):
    """Generates robots.txt dynamically."""
    return render(request, 'robots.txt', {}, content_type="text/plain")


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def update_resume(request):
    """Uploads a new ResumeFile and marks it as active."""
    if request.method == 'POST' and request.FILES.get('resume'):
        title = request.POST.get('title', 'S Sreesh Resume')
        uploaded = request.FILES['resume']
        resume_file = ResumeFile.objects.create(
            title=title or uploaded.name,
            file=uploaded,
            is_active=True
        )
        profile = Profile.objects.first()
        if profile:
            profile.resume = uploaded
            profile.save()
        return redirect('/admin-dashboard/?msg=resume_uploaded')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def set_active_resume(request, resume_id):
    """Sets a specific ResumeFile as active."""
    resume = get_object_or_404(ResumeFile, id=resume_id)
    resume.is_active = True
    resume.save()
    profile = Profile.objects.first()
    if profile and resume.file:
        profile.resume = resume.file
        profile.save()
    return redirect('/admin-dashboard/?msg=resume_activated')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_resume(request, resume_id):
    """Deletes a ResumeFile instance."""
    resume = get_object_or_404(ResumeFile, id=resume_id)
    resume.delete()
    return redirect('/admin-dashboard/?msg=resume_deleted')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def add_project(request):
    """Creates a new Project instance with optional Featured Project flag."""
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle', '')
        description = request.POST.get('description', '')
        long_description = request.POST.get('long_description', '')
        tech_stack = request.POST.get('tech_stack', '')
        github_url = request.POST.get('github_url', '')
        live_url = request.POST.get('live_url', '')
        is_featured = request.POST.get('is_featured') in ['on', 'true', '1']
        features_text = request.POST.get('features', '')
        challenges = request.POST.get('challenges', '')
        image = request.FILES.get('image')

        features_list = [f.strip() for f in features_text.split('\n') if f.strip()]

        project = Project.objects.create(
            title=title,
            subtitle=subtitle,
            description=description,
            long_description=long_description or description,
            tech_stack=tech_stack,
            github_url=github_url or None,
            live_url=live_url or None,
            is_featured=is_featured,
            features=json.dumps(features_list),
            challenges=challenges,
        )
        if image:
            project.image = image
            project.save()
        return redirect('/admin-dashboard/?msg=project_added')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_project(request, project_id):
    """Deletes a Project instance."""
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('/admin-dashboard/?msg=project_deleted')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def toggle_featured_project(request, project_id):
    """Toggles is_featured state for a Project."""
    project = get_object_or_404(Project, id=project_id)
    project.is_featured = not project.is_featured
    project.save()
    return redirect('/admin-dashboard/?msg=project_updated')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def update_project_url(request, project_id):
    """Updates the GitHub repository and Live URLs for a Project."""
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        github_url = request.POST.get('github_url', '').strip()
        live_url = request.POST.get('live_url', '').strip()
        project.github_url = github_url or None
        project.live_url = live_url or None
        project.save()
        return redirect('/admin-dashboard/?msg=project_url_updated')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def add_skill(request):
    """Adds a new Skill instance."""
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        proficiency = int(request.POST.get('proficiency', 80))
        icon_class = request.POST.get('icon_class', 'fa-solid fa-code')
        hover_glow = request.POST.get('hover_glow', '#00F5FF')

        Skill.objects.create(
            name=name,
            category=category,
            proficiency=proficiency,
            icon_class=icon_class,
            hover_glow=hover_glow
        )
        return redirect('/admin-dashboard/?msg=skill_added')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_skill(request, skill_id):
    """Deletes a Skill instance."""
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    return redirect('/admin-dashboard/?msg=skill_deleted')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def add_certificate(request):
    """Adds a new Certification instance."""
    if request.method == 'POST':
        name = request.POST.get('name')
        issuing_organization = request.POST.get('issuing_organization')
        issue_date = request.POST.get('issue_date')
        description = request.POST.get('description', '')
        credential_id = request.POST.get('credential_id', '')
        credential_url = request.POST.get('credential_url', '')

        Certification.objects.create(
            name=name,
            issuing_organization=issuing_organization,
            issue_date=issue_date,
            description=description,
            credential_id=credential_id,
            credential_url=credential_url
        )
        return redirect('/admin-dashboard/?msg=cert_added')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_certificate(request, cert_id):
    """Deletes a Certification instance."""
    cert = get_object_or_404(Certification, id=cert_id)
    cert.delete()
    return redirect('/admin-dashboard/?msg=cert_deleted')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def add_experience(request):
    """Adds a new Experience / Timeline entry."""
    if request.method == 'POST':
        role = request.POST.get('role')
        company = request.POST.get('company')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date', 'Present')
        achievements = request.POST.get('achievements', '')
        responsibilities = request.POST.get('responsibilities', '')
        is_current = request.POST.get('is_current') in ['on', 'true', '1']

        achievements_list = [a.strip() for a in achievements.split('\n') if a.strip()]
        responsibilities_list = [r.strip() for r in responsibilities.split('\n') if r.strip()]

        Experience.objects.create(
            role=role,
            company=company,
            start_date=start_date,
            end_date=end_date,
            achievements=json.dumps(achievements_list),
            responsibilities=json.dumps(responsibilities_list),
            is_current=is_current
        )
        return redirect('/admin-dashboard/?msg=exp_added')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_experience(request, exp_id):
    """Deletes an Experience instance."""
    exp = get_object_or_404(Experience, id=exp_id)
    exp.delete()
    return redirect('/admin-dashboard/?msg=exp_deleted')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def update_profile_pic(request):
    """Updates the main hero profile picture."""
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        img_dir = os.path.join(settings.MEDIA_ROOT, 'profile')
        os.makedirs(img_dir, exist_ok=True)
        
        # Clear existing profile image files
        for f in os.listdir(img_dir):
            file_path = os.path.join(img_dir, f)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

        uploaded = request.FILES['profile_pic']
        save_path = os.path.join(img_dir, uploaded.name)
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded.chunks():
                destination.write(chunk)

        profile = Profile.objects.first()
        if profile:
            profile.profile_pic = f'profile/{uploaded.name}'
            profile.save()

        return redirect('/admin-dashboard/?msg=pic_updated')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def add_about_photo(request):
    """Uploads a new photo to the About section slideshow gallery."""
    if request.method == 'POST' and request.FILES.get('about_photo'):
        img_dir = os.path.join(settings.MEDIA_ROOT, 'profile images')
        os.makedirs(img_dir, exist_ok=True)
        uploaded = request.FILES['about_photo']
        save_path = os.path.join(img_dir, uploaded.name)
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded.chunks():
                destination.write(chunk)
        return redirect('/admin-dashboard/?msg=photo_added')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_about_photo(request):
    """Deletes a photo from the About section slideshow gallery."""
    if request.method == 'POST':
        filename = request.POST.get('filename')
        if filename:
            file_path = os.path.join(settings.MEDIA_ROOT, 'profile images', filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
        return redirect('/admin-dashboard/?msg=photo_deleted')
    return redirect('/admin-dashboard/')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def update_about(request):
    """Updates About Section content (about_heading, bio, location, soft_skills, languages)."""
    if request.method == 'POST':
        profile = Profile.objects.first()
        if not profile:
            profile = Profile.objects.create(name="S Sreesh", email="ssreesh45@gmail.com")

        profile.about_heading = request.POST.get('about_heading', 'Developing Next-Gen Intelligent Stacks')
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', 'Kerala, India')
        profile.soft_skills = request.POST.get('soft_skills', '')
        profile.languages = request.POST.get('languages', '')
        profile.save()
        return redirect('/admin-dashboard/?msg=about_updated')
    return redirect('/admin-dashboard/')

