from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist


class MessageMixin(SuccessMessageMixin):
    success_message = "Success!"


class FilterOwnerMixin(object, ):
    def get_queryset(self, ):
        return super(FilterOwnerMixin, self).get_queryset().filter(
            created_by=self.request.user
        )


class AuditableMixin(object,):
    def form_valid(self, form, ):
        try:
            if not getattr(form.instance, 'created_by') and not form.instance.created_by:
                form.instance.created_by = self.request.user
        except ObjectDoesNotExist:
            form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super(AuditableMixin, self).form_valid(form)