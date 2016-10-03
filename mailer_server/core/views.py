from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import FormView

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mailer_server.core.forms import EmptyForm

import mailer_server.core.jobs
from mailer_server.core.serializers import MailSerializer

class CreateTokenFormView(FormView):
    form_class = EmptyForm
    template_name = 'create_token.html'

    def form_valid(self, form):
        # Delete old token
        Token.objects.filter(user=self.request.user).delete()
        # Create new one
        token = Token.objects.create(user=self.request.user)

        msg = mark_safe('A new access toekn has been created. Please copy its value because if you lose it you\'ll need to create it again: <br /><br /><b>{0}</b>'.format(token.key))
        messages.info(self.request, msg)

        return HttpResponseRedirect(reverse('home'))

@permission_required('core.admin')
def send_test_email(request):
    msg = mark_safe('Sending test email ...')
    messages.info(request, msg)
    mailer_server.core.jobs.send_test_email(request.user)
    return HttpResponseRedirect(reverse('home'))
    
    
class SendMailAPIView(APIView):
    #authentication_classes = (TokenAuthentication, )

    
    def get(self, request, format=None):
        serializer = MailSerializer(data=request.data)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MailSerializer(data=request.data)
        
        if serializer.is_valid():
            print serializer
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)