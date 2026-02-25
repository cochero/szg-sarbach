from django.urls import path
from . import views

urlpatterns = [
    path('appointment/', views.appointment_page, name='appointment'),
    path('appointment/submit/', views.appointment_submit, name='appointment_submit'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('user/', views.my_appointments, name='my_appointments'),
    path('myaddons/', views.my_addons, name='my_addons'),
    path('future-apps/', views.upcoming_appointments, name='upcoming_appointments'),
    path('old-apps/', views.past_appointments, name='past_appointments'),
    path('ajax/locations/', views.ajax_locations, name='ajax_locations'),
]
