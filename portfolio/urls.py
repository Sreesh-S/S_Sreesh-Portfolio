from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('skills/', views.skills, name='skills'),
    path('experience/', views.experience, name='experience'),
    path('certifications/', views.certifications, name='certifications'),
    path('contact/', views.contact, name='contact'),
    path('download-resume/', views.download_resume, name='download_resume'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/toggle-read/<int:message_id>/', views.toggle_message_read, name='toggle_message_read'),
    path('admin-dashboard/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('admin-dashboard/update-resume/', views.update_resume, name='update_resume'),
    path('admin-dashboard/set-active-resume/<int:resume_id>/', views.set_active_resume, name='set_active_resume'),
    path('admin-dashboard/delete-resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('admin-dashboard/add-project/', views.add_project, name='add_project'),
    path('admin-dashboard/delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('admin-dashboard/toggle-featured-project/<int:project_id>/', views.toggle_featured_project, name='toggle_featured_project'),
    path('admin-dashboard/update-project-url/<int:project_id>/', views.update_project_url, name='update_project_url'),
    path('admin-dashboard/add-skill/', views.add_skill, name='add_skill'),
    path('admin-dashboard/delete-skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('admin-dashboard/add-certificate/', views.add_certificate, name='add_certificate'),
    path('admin-dashboard/delete-certificate/<int:cert_id>/', views.delete_certificate, name='delete_certificate'),
    path('admin-dashboard/add-experience/', views.add_experience, name='add_experience'),
    path('admin-dashboard/delete-experience/<int:exp_id>/', views.delete_experience, name='delete_experience'),
    path('admin-dashboard/update-profile-pic/', views.update_profile_pic, name='update_profile_pic'),
    path('admin-dashboard/add-about-photo/', views.add_about_photo, name='add_about_photo'),
    path('admin-dashboard/delete-about-photo/', views.delete_about_photo, name='delete_about_photo'),
    path('admin-dashboard/update-about/', views.update_about, name='update_about'),
    path('ai-assistant/', views.ai_assistant, name='ai_assistant'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('search/', views.command_palette_search, name='command_palette_search'),
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('robots.txt', views.robots_view, name='robots'),
]

