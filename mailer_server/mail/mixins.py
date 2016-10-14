from django_tables2 import SingleTableMixin
import mailer_server.mail.tables


class MailTemplateTableMixin(SingleTableMixin, ):
    
    table_class = mailer_server.mail.tables.MailTemplateTable


class DistributionListTableMixin(SingleTableMixin, ):
    
    table_class = mailer_server.mail.tables.DistributionListTable

