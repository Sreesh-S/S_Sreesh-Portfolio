from django.contrib import admin
from .models import (
    Profile, Skill, Project, Experience, Education, 
    Certification, ContactMessage, Visitor, ResumeAnalytics, Blog, SocialLinks, ResumeFile
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_featured',)
    search_fields = ('title', 'tech_stack')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date')
    list_filter = ('company',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'field_of_study', 'institution', 'start_year', 'end_year')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'country', 'city', 'visit_time')
    list_filter = ('country', 'visit_time')

@admin.register(ResumeAnalytics)
class ResumeAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('download_time', 'ip_address')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'read_time')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url')

@admin.register(ResumeFile)
class ResumeFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'uploaded_at')
    list_filter = ('is_active',)


