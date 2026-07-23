from django.db import models
from django.utils.text import slugify
import json

class Profile(models.Model):
    name = models.CharField(max_length=100, default="S Sreesh")
    title = models.CharField(max_length=200, default="Software Developer | Python Developer")
    location = models.CharField(max_length=100, default="Kerala, India")
    email = models.EmailField(default="ssreesh45@gmail.com")
    phone = models.CharField(max_length=20, default="+91 81294 10562")
    linkedin = models.URLField(default="https://www.linkedin.com/in/s-sreesh")
    github = models.URLField(default="https://github.com/Sreesh-S")
    portfolio_url = models.URLField(default="https://sreesh-portfolio.vercel.app/")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile/', blank=True, null=True)
    about_heading = models.CharField(max_length=200, default="Developing Next-Gen Intelligent Stacks")
    bio = models.TextField(blank=True, null=True)
    languages = models.CharField(max_length=200, default="English, Malayalam, Hindi")
    soft_skills = models.CharField(max_length=300, default="Problem Solving, Analytical Thinking, Team Collaboration, Time Management, Continuous Learning")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Programming', 'Programming'),
        ('Web', 'Web Development'),
        ('Machine Learning', 'Machine Learning & AI'),
        ('Data', 'Data Analytics & Visualisation'),
        ('Database', 'Databases'),
        ('Tools', 'Tools & Devops'),
    ]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(help_text="Proficiency percentage (0-100)")
    icon_class = models.CharField(max_length=100, help_text="FontAwesome class e.g., 'fa-brands fa-python'")
    hover_glow = models.CharField(max_length=20, default="#00F5FF", help_text="Hex color code for glow, e.g., #00F5FF")

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(help_text="Short summary for listing card")
    long_description = models.TextField(help_text="Detailed description (supports markdown or HTML)")
    image = models.ImageField(upload_to='projects/')
    image2 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image3 = models.ImageField(upload_to='projects/', blank=True, null=True)
    tech_stack = models.CharField(max_length=300, help_text="Comma-separated tech names, e.g., Python, Django, ML")
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    case_study_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    features = models.TextField(help_text="JSON list of core features or line-separated text")
    challenges = models.TextField(blank=True, null=True)
    architecture_diagram = models.ImageField(upload_to='projects/architecture/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    def get_features_list(self):
        try:
            return json.loads(self.features)
        except Exception:
            return [f.strip() for f in self.features.split('\n') if f.strip()]

    def __str__(self):
        return self.title


class Experience(models.Model):
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    start_date = models.CharField(max_length=50, help_text="e.g., 'June 2024'")
    end_date = models.CharField(max_length=50, help_text="e.g., 'August 2024' or 'Present'")
    achievements = models.TextField(help_text="Line-separated achievements or JSON list")
    responsibilities = models.TextField(help_text="Line-separated responsibilities or JSON list")
    is_current = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='experience/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Ordering index")

    class Meta:
        ordering = ['order', '-id']

    def get_achievements_list(self):
        try:
            return json.loads(self.achievements)
        except Exception:
            return [a.strip() for a in self.achievements.split('\n') if a.strip()]

    def get_responsibilities_list(self):
        try:
            return json.loads(self.responsibilities)
        except Exception:
            return [r.strip() for r in self.responsibilities.split('\n') if r.strip()]

    def __str__(self):
        return f"{self.role} at {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_year = models.CharField(max_length=10)
    end_year = models.CharField(max_length=10, default="Present")
    grade = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-end_year']

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution}"


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.CharField(max_length=50, help_text="e.g., 'July 2024'")
    description = models.TextField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    hover_glow = models.CharField(max_length=20, default="#7B61FF")

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100, default="Unknown")
    city = models.CharField(max_length=100, default="Unknown")
    visit_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_time']

    def __str__(self):
        return f"Visitor from {self.city}, {self.country} on {self.visit_time}"


class ResumeAnalytics(models.Model):
    download_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        ordering = ['-download_time']

    def __str__(self):
        return f"Resume downloaded at {self.download_time} by {self.ip_address}"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_time = models.IntegerField(default=5, help_text="Estimated read time in minutes")
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SocialLinks(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=100, help_text="e.g., 'fa-brands fa-github'")

    def __str__(self):
        return self.platform


class ResumeFile(models.Model):
    title = models.CharField(max_length=150, default="S Sreesh Resume")
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate all other ResumeFiles
            ResumeFile.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

