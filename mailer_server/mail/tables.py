import django_tables2 as tables
from django_tables2.columns import LinkColumn, TemplateColumn
from django_tables2.utils import A
from mailer_server.mail.models import Mail, MassMail, DistributionList, MailTemplate


class DistributionListTable(tables.Table):
    id = LinkColumn('dl_mail_distributionlist_detail', args=[A('pk')])
    class Meta:
        model = DistributionList
        attrs = {'class': 'table'}


class MailTemplateTable(tables.Table):
    id = LinkColumn('mt_mail_mailtemplate_detail', args=[A('pk')])
    body = TemplateColumn("""{% if record.body_type == 'html' %}{{ record.body|safe }}{% else %}{{ record.body }}{% endif %}""", orderable=False,)

    class Meta:
        model = MailTemplate
        attrs = {'class': 'table'}


class MailTable(tables.Table):
    mail_template = LinkColumn('mt_mail_mailtemplate_detail', args=[A('mail_template_id')])
        
    class Meta:
        model = Mail
        attrs = {'class': 'table'}
        order_by = ('-id', )


class MassMailTable(tables.Table):
    mail_template = LinkColumn('mt_mail_mailtemplate_detail', args=[A('mail_template_id')])
    distribution_list_to = LinkColumn('dl_mail_distributionlist_detail', args=[A('distribution_list_to_id')])

    class Meta:
        model = MassMail
        attrs = {'class': 'table'}
        order_by = ('-id', )