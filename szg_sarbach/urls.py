from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('appointments.urls')),
    path('', include('shop.urls')),
    path('', include('blog_app.urls')),
    path('panel/', include('admin_panel.urls')),
    path('', include('clinic.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
