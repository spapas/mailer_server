from django import forms
from mailer_server.mail import models
from extra_views import InlineFormSet
from dal import autocomplete

import unicodecsv as csv

from mailer_server.mail import models

class EmailAddressInline(InlineFormSet):
    model = models.EmailAddress
    fields = ('name', 'email', )
    factory_kwargs = {'extra': 1, }
    # extra=1
    
    
class MailAttachmentInline(InlineFormSet):
    model = models.MailAttachment
    fields = ('name', 'content', )
    factory_kwargs = {'extra': 1, }
    # extra=1
    

class DistributionListForm(forms.ModelForm):
    class Meta:
        fields = ('name',  )
        model = models.DistributionList

        
class MailTemplateForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'subject', 'body', 'body_type', 'mail_from', 'reply_to', )
        model = models.MailTemplate         

        
class SendMailForm(forms.Form):
    distribution_list = forms.ModelChoiceField(
        queryset=models.DistributionList.objects.all(),
        widget=autocomplete.ModelSelect2(url='distributionlist-autocomplete')
    )
    
    mail_template = forms.ModelChoiceField(
        queryset=models.MailTemplate.objects.all(),
        widget=autocomplete.ModelSelect2(url='mailtemplate-autocomplete')
    )


class SendMailConfirmForm(forms.Form):
    distribution_list = forms.ModelChoiceField(
        queryset=models.DistributionList.objects.all(),
        widget=forms.HiddenInput()
    )
    
    mail_template = forms.ModelChoiceField(
        queryset=models.MailTemplate.objects.all(),
        widget=forms.HiddenInput()
    )
   
    
class UploadDistributionListForm(forms.ModelForm):
    file = forms.FileField(label='CSV file', help_text='Please upload a CSV file with the emails of the distribution list')
    
    class Meta:
        fields = ()
        model = models.DistributionList
   
    def clean(self):
        data = super(UploadDistributionListForm, self).clean()
        fin = data['file']
        if fin.name[-3:].lower() != 'csv':
            raise forms.ValidationError("Please use a CSV file!")
        reader = csv.reader(fin, encoding='utf-8', delimiter=',', quotechar='"')
        self.emails = []
        for idx, row in enumerate(reader):
            if idx==0:
                # Skip headers
                continue 
            self.emails.append(models.EmailAddress(
                name=row[0],
                email=row[1],
                distribution_list=self.instance,
            ))
            

class MailForm(forms.ModelForm):
    mail_to = forms.CharField(help_text='Enter a list of cc separated with commas (,)', required=False,)
    cc = forms.CharField(help_text='Enter a list of cc separated with commas (,)', required=False,)
    bcc = forms.CharField(help_text='Enter a list of cc separated with commas (,)', required=False,)

    class Meta:
        fields = ('subject', 'body_type', 'body', 'mail_from' ,'reply_to', 'mail_to', 'cc', 'bcc', )
        model = models.Mail

    def __init__(self, *args, **kwargs):
        super(MailForm, self).__init__(*args, **kwargs)
        self.fields['subject'].required = True
        self.fields['body'].required = True

    def clean(self):
        data = super(MailForm, self).clean()

        tot_addrs = 0 
        #tot_addrs += len(data.get('mail_to', '').split(','))
        #tot_addrs += len(data.get('cc', '').split(','))
        #tot_addrs += len(data.get('bcc', '').split(','))
        #a+=1
        if not data.get('mail_to') and not data.get('cc') and not data.get('bcc'):
            msg = "Please enter at least one email address!"
            self._errors['mail_to'] = self.error_class([msg])
            self._errors['cc'] = self.error_class([msg])
            self._errors['bcc'] = self.error_class([msg])
            
        return data