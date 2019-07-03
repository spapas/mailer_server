import django_filters
from mailer_server.mail import models


class MailFilter(django_filters.FilterSet):
    class Meta:
        model = models.Mail
        fields = {
            'mail_from': ['icontains'], 
            'reply_to': ['icontains'], 
            'mail_to': ['icontains'], 
            'subject': ['icontains'], 
            'body': ['icontains'], 
            'created_by__username': ['icontains'], 
            'mail_template__name': ['icontains'],
        }
        
        
class MassMailFilter(django_filters.FilterSet):
    class Meta:
        model = models.MassMail
        fields = {
            'mail_template__name': ['icontains'], 
            'distribution_list_to__name': ['icontains'], 
            'created_by__username': ['icontains'], 
        }
        
        
class DistributionListFilter(django_filters.FilterSet):
    class Meta:
        model = models.DistributionList
        fields = {
            'name': ['icontains'], 
            'created_by__username': ['icontains'], 
            
        }
        
        
class MailTemplateFilter(django_filters.FilterSet):
    class Meta:
        model = models.MailTemplate
        fields = {
            'name': ['icontains'], 
            'created_by__username': ['icontains'], 
            'mail_from': ['icontains'], 
            'reply_to': ['icontains'], 
            'subject': ['icontains'], 
            'body': ['icontains'], 
        }        