from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('realestate/', views.realestate, name='realestate'),
    path('register/', views.register_page, name='register'),
    path('ajax/patient-login/', views.patient_login, name='patient_login'),
    path('ajax/patient-register/', views.patient_register, name='patient_register'),
    path('doctor/', views.doctor_login_page, name='doctor_login_page'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('welcome/admin/', views.admin_login_page, name='admin_login_page'),
    path('welcome/adminlogin/', views.admin_login, name='admin_login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/change-password/', views.change_password, name='change_password'),
]
