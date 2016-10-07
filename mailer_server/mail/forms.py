from django import forms
from mailer_server.mail import models
from extra_views import InlineFormSet


class EmailAddressInline(InlineFormSet):
    model = models.EmailAddress
    fields = ('name', 'email', )

class DistributionListForm(forms.ModelForm):
    class Meta:
        fields = ('name',  )
        model = models.DistributionList