"""
mailer_server URL Configuration
"""
from django.conf import settings
from django.urls import re_path, include 
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    re_path(r'^', include('mailer_server.core.urls')),
    re_path(r'^mail/', include('mailer_server.mail.urls')),
    re_path(r'^admin/django-rq/', include('django_rq.urls')),
    re_path(r'^admin/', admin.site.urls),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]