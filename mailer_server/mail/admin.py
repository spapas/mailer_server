from django.contrib import admin
from mailer_server.mail.models import Mail, EmailAddress, DistributionList


class MailAdmin(admin.ModelAdmin):
    list_display = ("id", "created_on", "created_by", "mail_from", "mail_to", "subject")
    search_fields = (
        "created_by",
        "mail_from",
        "mail_to",
        "subject",
    )
    readonly_fields = (
        "created_on",
        "created_by",
        "mail_from",
        "mail_to",
        "cc",
        "bcc",
        "body_type",
        "mail_template",
        "reply_to",
        "subject",
        "body",
        "attachments",
    )


class NamedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


admin.site.register(Mail, MailAdmin)
admin.site.register(EmailAddress, NamedAdmin)
admin.site.register(DistributionList, NamedAdmin)