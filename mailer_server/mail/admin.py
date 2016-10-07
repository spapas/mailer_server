from django.contrib import admin
from mailer_server.mail.models import Mail

class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'created_by', 'mail_from', 'mail_to', 'subject')
    search_fields = ( 'created_by', 'mail_from', 'mail_to', 'subject', )

    
admin.site.register(Mail, MailAdmin)