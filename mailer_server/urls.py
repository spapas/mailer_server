"""
mailer_server URL Configuration
"""
from django.conf import settings
from django.conf.urls import url, include 
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('mailer_server.core.urls')),
    url(r'^mail/', include('mailer_server.mail.urls')),
    url(r'^admin/django-rq/', include('django_rq.urls')),
    url(r'^admin/', admin.site.urls),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]