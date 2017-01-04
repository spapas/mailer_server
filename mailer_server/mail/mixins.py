from django_tables2 import SingleTableMixin
import mailer_server.mail.tables


class FilteredSingleTableMixin(SingleTableMixin, ):
    def get_table_data(self):
        self.filter = self.filter_class(self.request.GET, queryset=super(FilteredSingleTableMixin, self).get_table_data() )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(FilteredSingleTableMixin, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        return context   


class MailTemplateTableMixin(FilteredSingleTableMixin, ):
    table_class = mailer_server.mail.tables.MailTemplateTable
    filter_class = mailer_server.mail.filters.MailTemplateFilter
    

class DistributionListTableMixin(FilteredSingleTableMixin, ):
    filter_class = mailer_server.mail.filters.DistributionListFilter
    table_class = mailer_server.mail.tables.DistributionListTable
    


