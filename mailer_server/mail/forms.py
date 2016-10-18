from django import forms
from mailer_server.mail import models
from extra_views import InlineFormSet
from dal import autocomplete

import unicodecsv as csv

from mailer_server.mail import models

class EmailAddressInline(InlineFormSet):
    model = models.EmailAddress
    fields = ('name', 'email', )
    extra=1
    
    
class MailAttachmentInline(InlineFormSet):
    model = models.MailAttachment
    fields = ('name', 'content', )
    extra=1
    

class DistributionListForm(forms.ModelForm):
    class Meta:
        fields = ('name',  )
        model = models.DistributionList

        
class MailTemplateForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'subject', 'body', 'body_type', 'mail_from', 'reply_to', )
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
    
    
class UploadDistributionListForm(forms.ModelForm):
    file = forms.FileField(label='CSV file', help_text='Please upload a CSV file with the emails of the distribution list')
    
    class Meta:
        fields = ()
        model = models.DistributionList
   
    def clean(self):
        fin = self.cleaned_data['file']
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
            
