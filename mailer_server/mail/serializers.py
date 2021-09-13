from rest_framework import serializers
from email.utils import parseaddr
from mailer_server.mail.models import Mail, MassMail


def email_valid(s):
    _, email = parseaddr(s)
    if email == '' or not '@' in email:
        return False
    return True


class MailSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(write_only=True, required=False, )

    class Meta:
        model = Mail
        fields = (
            'id', 'subject', 'body', 'mail_from',
            'mail_to', 'cc', 'bcc', 'body_type',
            'created_on', 'created_by', 'reply_to', 'attachment',

        )
        read_only_fields = ('id', 'created_on', 'created_by',)

    def validate(self, data):
        for f in ['mail_from', 'reply_to']:
            fval = data.get(f)
            if fval:
                if not email_valid(fval):
                    raise serializers.ValidationError("Cannot parse address {0}".format(fval))

        for f in ['mail_to', 'cc', 'bcc']:
            
            fval = data.get(f)
            print(f, fval)
            if fval:
                fval_parts = fval.split(',')
                for fvp in fval_parts:
                    print("Field original val and parsed ", fvp, parseaddr(fvp))
                    if not email_valid(fvp):
                        raise serializers.ValidationError("Cannot parse address {0}".format(fvp))
        return data


class MassMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MassMail
        fields = (
            'id', 'mail_template', 
            'distribution_list_to', 'created_on', 'created_by',

        )
        read_only_fields = ('id', 'created_on', 'created_by',)

