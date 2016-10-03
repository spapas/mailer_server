from django.conf import settings
from django.conf.urls import url, include 
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from mailer_server.core.views import CreateTokenFormView, send_test_email, SendMailAPIView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    
    url(r'send_test_email$', send_test_email, name='send_test_email'),
    url(r'create_token$', CreateTokenFormView.as_view(template_name='create_token.html'), name='create_token'),
    
    url(r'^api/send_mail/$', SendMailAPIView.as_view(), name='api_send_mail', ),
    
    url(r'login/$', login, name='auth_login'),
    url(r'logout/$', logout, {'template_name': 'logout.html'}, name='auth_logout'),

]
