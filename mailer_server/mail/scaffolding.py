from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect

from generic_scaffold import CrudManager
import mailer_server.mail.models
import mailer_server.mail.forms
import mailer_server.mail.mixins
import mailer_server.core.mixins

from extra_views import CreateWithInlinesView, UpdateWithInlinesView

user_permission_required = permission_required('core.user')



class DistributionListCreateView(CreateWithInlinesView):
    model = mailer_server.mail.models.DistributionList
    inlines = [mailer_server.mail.forms.EmailAddressInline, ]

    def forms_valid(self, form, inlines):
        dl = form.save(commit=False)
        dl.created_by = self.request.user
        dl.save()
        self.object = dl
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_absolute_url()


class DistributionListUpdateView(UpdateWithInlinesView):
    model = mailer_server.mail.models.DistributionList
    inlines = [mailer_server.mail.forms.EmailAddressInline, ]

    def forms_valid(self, form, inlines):
        dl = form.save(commit=False)
        dl.created_by = self.request.user
        dl.save()
        self.object = dl
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(DistributionListUpdateView, self).get_context_data(**kwargs)
        return context


class DistributionListCrudManager(CrudManager):
    model = mailer_server.mail.models.DistributionList
    form_class = mailer_server.mail.forms.DistributionListForm
    prefix = 'dl'

    #list_mixins = [core.mixins.MissionTableMixin, core.mixins.ExportTableMixin]
    create_mixins = [mailer_server.core.mixins.MessageMixin]

    update_mixins = [mailer_server.core.mixins.MessageMixin, mailer_server.core.mixins.FilterOwnerMixin]
    detail_mixins = [mailer_server.core.mixins.FilterOwnerMixin]
    list_mixins = [mailer_server.core.mixins.FilterOwnerMixin, mailer_server.mail.mixins.DistributionListTableMixin]
    delete_mixins = [mailer_server.core.mixins.FilterOwnerMixin]

    create_view_class = DistributionListCreateView
    update_view_class = DistributionListUpdateView

    permissions = {
        'list': user_permission_required,
        'update': user_permission_required,
        'delete': user_permission_required,
        'create': user_permission_required,
        'detail': user_permission_required,
    }
    
    



class MailTemplateCrudManager(CrudManager):
    model = mailer_server.mail.models.MailTemplate
    form_class = mailer_server.mail.forms.MailTemplateForm
    prefix = 'mt'

    create_mixins = [mailer_server.core.mixins.MessageMixin, mailer_server.core.mixins.AuditableMixin]

    update_mixins = [mailer_server.core.mixins.MessageMixin, mailer_server.core.mixins.FilterOwnerMixin, mailer_server.core.mixins.AuditableMixin]
    detail_mixins = [mailer_server.core.mixins.FilterOwnerMixin]
    list_mixins = [mailer_server.core.mixins.FilterOwnerMixin, mailer_server.mail.mixins.MailTemplateTableMixin]
    delete_mixins = [mailer_server.core.mixins.FilterOwnerMixin]

    permissions = {
        'list': user_permission_required,
        'update': user_permission_required,
        'delete': user_permission_required,
        'create': user_permission_required,
        'detail': user_permission_required,
    }