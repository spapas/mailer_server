from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from mailer_server.core.views import CreateTokenFormView

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    re_path(r'^help/$', TemplateView.as_view(template_name='help.html'), name='help'),
    re_path(r'create_token$', CreateTokenFormView.as_view(template_name='create_token.html'), name='create_token'),
    re_path(r'login/$', auth_views.LoginView.as_view(), name='auth_login'),
    re_path(r'logout/$', auth_views.LogoutView.as_view(template_name='logout.html'), name='auth_logout'),
    re_path(r'error/$', permission_required('core.admin')(lambda r: a+1), name='error')
]
