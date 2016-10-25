import django_tables2 as tables
from django_tables2.columns import LinkColumn
from django_tables2.utils import A
from mailer_server.mail.models import Mail, MassMail, DistributionList, MailTemplate


class DistributionListTable(tables.Table):
    id = LinkColumn('dl_mail_distributionlist_detail', args=[A('pk')])
    class Meta:
        model = DistributionList
        attrs = {'class': 'table'}


class MailTemplateTable(tables.Table):
    id = LinkColumn('mt_mail_mailtemplate_detail', args=[A('pk')])
    class Meta:
        model = MailTemplate
        attrs = {'class': 'table'}


class MailTable(tables.Table):
    class Meta:
        model = Mail
        attrs = {'class': 'table'}
        order_by = ('-created_on', )


class MassMailTable(tables.Table):
    class Meta:
        model = MassMail
        attrs = {'class': 'table'}