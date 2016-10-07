from django.contrib.messages.views import SuccessMessageMixin

class MessageMixin(SuccessMessageMixin):
    success_message = "Success!"