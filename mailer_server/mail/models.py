from __future__ import unicode_literals
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db import models

BODY_TYPE_CHOICES = (
    ('plain', 'plain text',),
    ('html', 'HTML' ,),
)


class NamedModel(models.Model):
    name = models.CharField(max_length=128, help_text='Please enter a name for this object', )

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Mail(models.Model):
    "A model to save sent mails in the database"
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    mail_template = models.ForeignKey('MailTemplate', blank=True, null=True, )

    subject = models.TextField(blank=True, null=True, )
    body = models.TextField(blank=True, null=True, )

    mail_from = models.CharField(max_length=255, blank=True, null=True, )
    reply_to = models.CharField(max_length=255, blank=True, null=True, )

    mail_to = models.TextField(help_text='Enter a list of receipients separated with commas (,)', blank=True, null=True,)
    cc = models.TextField(blank=True, null=True, help_text='Enter a list of cc separated with commas (,)' )
    bcc = models.TextField(blank=True, null=True, help_text='Enter a list of bcc separated with commas (,)' )
    body_type = models.CharField(choices=BODY_TYPE_CHOICES, max_length=32, default='plain', )

    def __unicode__(self):
        return u'{0} {1} {2} {3}'.format(self.created_on, created_by, self.id, self.subject)

    def get_tuple(self):
        return (
            self.subject,
            self.body,
            self.mail_from,
            self.mail_to.split(','),
        )

    def get_email_object(self, connection=None, attachments=None):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.mail_from,
            to=self.mail_to.split(',')  if self.to else None,,
            bcc=self.bcc.split(',') if self.bcc else None,
            connection=connection,
            attachments=attachments,
            cc=self.cc.split(',') if self.cc else None,
            reply_to=self.reply_to.split(',') if self.reply_to else None,

        )

        email.content_subtype = self.body_type
        return email


class MassMail(models.Model):
    "A model to save sent mass mails in the database"
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    mail_template = models.ForeignKey('MailTemplate')

    distribution_list_to = models.ForeignKey('DistributionList')

    def get_mails(self):
        mail_list = []
        for address in self.distribution_list_to.emailaddress_set.all():
            mail = self.mail_template.get_mail_object()
            mail.created_by = self.created_by
            mail.mail_to = address.email

            mail_list.append(mail)
        return mail_list

    def get_emails(self):
        email_list = []
        for address in self.distribution_list_to.emailaddress_set.all():
            email = self.mail_template.get_email_object()
            email.to = [address.email]
            email_list.append(email)
        return email_list


class EmailAddress(NamedModel):
    "A simple model for an email address"
    email = models.EmailField()
    distribution_list = models.ForeignKey('DistributionList')


class DistributionList(NamedModel):
    "A list of  emails to be used later"
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_absolute_url(self):
        return reverse('dl_mail_distributionlist_detail', args=[self.id] )


class MailTemplate(NamedModel):
    "A model to save emails to be send later"
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    subject = models.TextField(help_text='Enter the subject of this template', )
    body = models.TextField(help_text='Enter the body of this template - can be either plain text or html depending on body type')

    mail_from = models.EmailField(blank=True, null=True, help_text='Enter a mail from - you may leave it empty to use the default mail from',)
    reply_to = models.EmailField(blank=True, null=True, help_text='Enter an optional reply to email',)

    body_type = models.CharField(choices=BODY_TYPE_CHOICES, max_length=32, default='plain', )

    def get_absolute_url(self):
        return reverse('mt_mail_mailtemplate_detail', args=[self.id] )

    def get_mail_object(self):
        return Mail(
            mail_template=self,
            subject=self.subject[:32],
            body=self.body[:32],
            mail_from=self.mail_from,
            reply_to=self.reply_to,
            body_type=self.body_type,
        )

    def get_email_object(self):
        attachments = [(x.name, x.content.read(), x.content_type) for x in self.mailattachment_set.all()]
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.mail_from,
            attachments=attachments,
            reply_to=[self.reply_to],
        )

        email.content_subtype = self.body_type
        return email


class MailAttachment(NamedModel):
    mail_template = models.ForeignKey('MailTemplate')
    content = models.FileField(help_text='Pick a file to use as the content of this mail attachment')
    content_type = models.CharField(max_length=128, default='text/plain', )
