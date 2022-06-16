from django.conf import settings
from django.conf.urls import url, include 
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from mailer_server.core.views import CreateTokenFormView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^help/$', TemplateView.as_view(template_name='help.html'), name='help'),
    
    url(r'create_token$', CreateTokenFormView.as_view(template_name='create_token.html'), name='create_token'),
    
    url(r'login/$', auth_views.LoginView.as_view(), name='auth_login'),
    url(r'logout/$', auth_views.LogoutView.as_view(template_name='logout.html'), name='auth_logout'),

    url(r'error/$', permission_required('core.admin')(lambda r: a+1), name='error')
]
