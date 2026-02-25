from django.urls import path
from . import views

urlpatterns = [
    path('treatment/<slug:slug>/', views.treatment_detail, name='treatment_detail'),
    path('doctor-profile/', views.doctor_profile, name='doctor_profile'),
    path('accomodations/', views.accommodations, name='accommodations'),
    path('apartment/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('packages/', views.package_list, name='packages'),
    path('package/<slug:slug>/', views.package_detail, name='package_detail'),
    path('addons/', views.addon_list, name='addons'),
    path('ajax/treatments/', views.ajax_treatments, name='ajax_treatments'),
    path('departments/<slug:slug>/', views.department_list, name='department_list'),
]
