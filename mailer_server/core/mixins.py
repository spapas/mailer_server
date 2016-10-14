from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist


class MessageMixin(SuccessMessageMixin):
    success_message = "Success!"


class FilterOwnerMixin(object, ):
    def get_queryset(self, ):
        qs = super(FilterOwnerMixin, self).get_queryset()
        
        # Admin sees all objects
        if self.request.user.has_perm('core.admin'):
            return  qs 
            
        # Other users see only their own
        return qs.filter(
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