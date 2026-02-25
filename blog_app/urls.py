from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.blog_list, {'post_type': 'Blog'}, name='blogs'),
    path('events/', views.blog_list, {'post_type': 'Event'}, name='events'),
    path('workshops/', views.blog_list, {'post_type': 'WorkShop'}, name='workshops'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('event/<slug:slug>/', views.blog_detail, name='event_detail'),
    path('workshop/<slug:slug>/', views.blog_detail, name='workshop_detail'),
]
