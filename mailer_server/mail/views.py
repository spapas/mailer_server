from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.fields import CurrentUserDefault
from rest_framework.views import APIView
from rest_framework.response import Response

from dal import autocomplete

from mailer_server.mail import jobs
from mailer_server.mail.serializers import MailSerializer

from mailer_server.mail import models 
from mailer_server.mail import forms


class UserPermissionRequiredMixin(PermissionRequiredMixin, ):
    permission_required = 'core.user'


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
        

class SendMassMailFormView(UserPermissionRequiredMixin, FormView):
    form_class = forms.SendMailForm
    template_name = 'send_mail.html'
    
    def form_valid(self, form):
        
        if jobs.send_mass_mail(form, self.request.user):
            messages.info(self.request, 'Started sending emails!')
        else:
            messages.info(self.request, 'Not able to send any emails!')
            
        return HttpResponseRedirect(reverse('home')) 
        

class DistributionListAutocomplete(UserPermissionRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return DistributionList.objects.none()

        qs = models.DistributionList.objects.filter(created_by=self.request.user) 

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
        
        
class MailTemplateAutocomplete(UserPermissionRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return MailTemplate.objects.none()

        qs = models.MailTemplate.objects.filter(created_by=self.request.user) 

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
        
        
        