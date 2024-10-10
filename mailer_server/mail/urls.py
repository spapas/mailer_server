from django.conf import settings
from django.urls import re_path
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
    re_path(r'send_test_email$', send_test_email, name='send_test_email'),
    re_path(r'^api/list_mail/$', MailListAPIView.as_view(), name='api_list_mail', ),   
    re_path(r'^api/send_mail/$', SendMailAPIView.as_view(), name='api_send_mail', ),   
    re_path(r'^api/send_mass_mail/$', SendMassMailAPIView.as_view(), name='api_send_mass_mail', ),   
    re_path(r'send_mail$', SendMailCreateView.as_view(), name='send_mail'),
    re_path(r'send_mass_mail$', SendMassMailFormView.as_view(), name='send_mass_mail'),
    re_path(r'send_mass_mail_confirm$', SendMassMailConfirmFormView.as_view(), name='send_mass_mail_confirm'),
    re_path(r'^dlupload/(?P<pk>\d+)/$', UploadDistributionListView.as_view(), name='dl_upload'),
    re_path(r'^dldownload/(?P<pk>\d+)/$', DownloadDistributionListView.as_view(), name='dl_download'),
    re_path(r'^mail_list/$', MailListView.as_view(), name='mail_list'),
    re_path(r'^mass_mail_list/$', MassMailListView.as_view(), name='mass_mail_list'),
    re_path(r'^distributionlist-autocomplete/$', DistributionListAutocomplete.as_view(), name='distributionlist-autocomplete', ),
    re_path(r'^mailtemplate-autocomplete/$', MailTemplateAutocomplete.as_view(), name='mailtemplate-autocomplete', ),
    
    
]


dl_crud = DistributionListCrudManager()
mt_crud = MailTemplateCrudManager()

urlpatterns += dl_crud.get_url_patterns()
urlpatterns += mt_crud.get_url_patterns()