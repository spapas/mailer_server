from django.conf import settings
from django.conf.urls import url, include 
from django.conf.urls.static import static
from django.contrib import admin

from django.views.generic import TemplateView

from mailer_server.mail.views import (
    send_test_email, SendMailAPIView, DistributionListAutocomplete, 
    MailTemplateAutocomplete, SendMassMailFormView, SendMassMailAPIView, UploadDistributionListView,
    DownloadDistributionListView, MailListView, MassMailListView, SendMassMailConfirmFormView, SendMailCreateView,
    MailListAPIView
)
from mailer_server.mail.scaffolding import DistributionListCrudManager, MailTemplateCrudManager

urlpatterns = [
    url(r'send_test_email$', send_test_email, name='send_test_email'),
    url(r'^api/list_mail/$', MailListAPIView.as_view(), name='api_list_mail', ),   
    url(r'^api/send_mail/$', SendMailAPIView.as_view(), name='api_send_mail', ),   
    url(r'^api/send_mass_mail/$', SendMassMailAPIView.as_view(), name='api_send_mass_mail', ),   

    url(r'send_mail$', SendMailCreateView.as_view(), name='send_mail'),
    
    url(r'send_mass_mail$', SendMassMailFormView.as_view(), name='send_mass_mail'),
    url(r'send_mass_mail_confirm$', SendMassMailConfirmFormView.as_view(), name='send_mass_mail_confirm'),
    
    url(r'^dlupload/(?P<pk>\d+)/$', UploadDistributionListView.as_view(), name='dl_upload'),
    url(r'^dldownload/(?P<pk>\d+)/$', DownloadDistributionListView.as_view(), name='dl_download'),
    
    url(r'^mail_list/$', MailListView.as_view(), name='mail_list'),
    url(r'^mass_mail_list/$', MassMailListView.as_view(), name='mass_mail_list'),
    
    url(r'^distributionlist-autocomplete/$', DistributionListAutocomplete.as_view(), name='distributionlist-autocomplete', ),
    url(r'^mailtemplate-autocomplete/$', MailTemplateAutocomplete.as_view(), name='mailtemplate-autocomplete', ),
    
    
]


dl_crud = DistributionListCrudManager()
mt_crud = MailTemplateCrudManager()

urlpatterns += dl_crud.get_url_patterns()
urlpatterns += mt_crud.get_url_patterns()