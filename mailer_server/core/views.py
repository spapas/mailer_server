from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import FormView

from rest_framework.authtoken.models import Token

from mailer_server.core.forms import EmptyForm


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
