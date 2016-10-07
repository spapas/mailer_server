from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

BODY_TYPE_CHOICES = (
    ('plain', 'plain text',),
    ('html', 'HTML' ,),
)


class NamedModel(models.Model):
    name = models.CharField(max_length=128, )

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Mail(models.Model):
    # A model to save sent mails in the database
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    subject = models.TextField()
    body = models.TextField()

    mail_from = models.EmailField()
    mail_to = models.TextField()
    cc = models.TextField(blank=True, null=True,)
    bcc = models.TextField(blank=True, null=True,)
    body_type = models.CharField(choices=BODY_TYPE_CHOICES, max_length=32, default='plain', )


class EmailAddress(NamedModel):
    email = models.EmailField()
    distribution_list = models.ForeignKey('DistributionList')


class DistributionList(NamedModel):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_absolute_url(self):
        return reverse('dl_mail_distributionlist_detail', args=[self.id] )