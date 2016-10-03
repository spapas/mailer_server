from rest_framework import serializers


class MailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    body = serializers.CharField()
    
    mail_from = serializers.CharField()
    mail_to = serializers.CharField()
    cc = serializers.CharField(required=False, )
    bcc = serializers.CharField(required=False, )
    body_type = serializers.CharField(default='plain')
    
    
