from django import forms
from mailer_server.mail import models
from extra_views import InlineFormSet


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
