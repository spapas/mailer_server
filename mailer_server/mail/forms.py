from django import forms
from mailer_server.mail import models
from extra_views import InlineFormSet
from dal import autocomplete

from mailer_server.mail import models

class EmailAddressInline(InlineFormSet):
    model = models.EmailAddress
    fields = ('name', 'email', )
    extra=1
    

class DistributionListForm(forms.ModelForm):
    class Meta:
        fields = ('name',  )
        model = models.DistributionList

        
class MailTemplateForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'subject', 'body', 'body_type', )
        model = models.MailTemplate

        
class SendMailForm(forms.Form):
    from_address = forms.EmailField()

    distribution_list = forms.ModelChoiceField(
        queryset=models.DistributionList.objects.all(),
        widget=autocomplete.ModelSelect2(url='distributionlist-autocomplete')
    )
    
    mail_template = forms.ModelChoiceField(
        queryset=models.MailTemplate.objects.all(),
        widget=autocomplete.ModelSelect2(url='mailtemplate-autocomplete')
    )
    