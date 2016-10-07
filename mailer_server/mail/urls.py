from django.conf import settings
from django.conf.urls import url, include 
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from mailer_server.mail.views import send_test_email, SendMailAPIView

urlpatterns = [
    
    url(r'send_test_email$', send_test_email, name='send_test_email'),
    url(r'^api/send_mail/$', SendMailAPIView.as_view(), name='api_send_mail', ),
    
]
