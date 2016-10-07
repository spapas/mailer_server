from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.fields import CurrentUserDefault
from rest_framework.views import APIView
from rest_framework.response import Response

from mailer_server.mail import jobs
from mailer_server.mail.serializers import MailSerializer


@permission_required('core.admin')
def send_test_email(request):
    msg = mark_safe('Sending test email ...')
    messages.info(request, msg)
    jobs.send_test_mail(request.user)
    return HttpResponseRedirect(reverse('home'))
    
    
class SendMailAPIView(APIView):
    #authentication_classes = (TokenAuthentication, )

    def get(self, request, format=None):
        serializer = MailSerializer(data=request.data)
        return Response(serializer.data)

    def post(self, request, format=None):
        print request.data
        
        serializer = MailSerializer(data=request.data, )
        if serializer.is_valid():
            
            mail = serializer.save(created_by=self.request.user)
            jobs.send_mail(mail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)