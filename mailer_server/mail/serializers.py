from rest_framework import serializers

from mailer_server.mail.models import Mail

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = (
            'id', 'subject', 'body', 'mail_from',
            'mail_to', 'cc', 'bcc', 'body_type',
            'created_on', 'created_by',

        )
        read_only_fields = ('id', 'created_on', 'created_by',)

